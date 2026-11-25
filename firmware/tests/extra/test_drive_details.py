import unittest, sys
import io
import json
import runpy
import types
from unittest.mock import patch
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from drive_logic import DriveController, mix

class DriveTests(unittest.TestCase):
    def command(self, **changes):
        data=dict(cmd='drive',armed=True,resume=True,vx=.5,vy=0,wz=0)
        data.update(changes)
        return data

    def test_resume_flag_must_be_boolean(self):
        for value in (None, 0, 1, 'true', [], {}):
            with self.subTest(resume=value):
                c = DriveController()
                c.receive(self.command(), 0)
                self.assertFalse(c.receive(self.command(resume=value), 100))
                self.assertEqual(c.output(100), (0, 0, 0, 0))
                self.assertFalse(c.receive(self.command(resume=False), 200))
        c = DriveController()
        self.assertFalse(c.receive(self.command(vx=2), 0))
        self.assertFalse(c.armed)

    def test_invalid_receive_time_latches_stop_without_rewinding_clock(self):
        for bad in (True, -1, 1.5, float('nan'), 99):
            with self.subTest(time=bad):
                c = DriveController()
                c.receive(self.command(), 100)
                self.assertFalse(c.receive(self.command(), bad))
                self.assertEqual(c.updated_ms, 100)
                self.assertFalse(c.receive(self.command(resume=False), 200))
                self.assertEqual(c.output(200), (0, 0, 0, 0))
                self.assertTrue(c.receive(self.command(), 300))

    def test_invalid_output_time_stops_and_cannot_be_used_to_resume(self):
        for bad in (True, -1, 1.5, float('inf'), 99):
            c = DriveController()
            c.receive(self.command(), 100)
            self.assertEqual(c.output(bad), (0, 0, 0, 0))
            self.assertEqual(c.updated_ms, 100)
            self.assertFalse(c.receive(self.command(resume=False), 200))
            self.assertTrue(c.receive(self.command(), 300))

    def test_configuration_rejects_invalid_watchdogs_and_output_limits(self):
        for options in (dict(timeout_ms=0), dict(timeout_ms=-1),
                        dict(timeout_ms=True), dict(timeout_ms=1.5),
                        dict(max_output=-.1), dict(max_output=1.01),
                        dict(max_output=True), dict(max_output=float('nan')),
                        dict(max_output=float('inf')), dict(max_output='0.2')):
            with self.subTest(options=options), self.assertRaises(ValueError):
                DriveController(**options)
        c = DriveController(max_output=0)
        self.assertTrue(c.receive(self.command(), 0))
        self.assertEqual(c.output(0), (0, 0, 0, 0))


class PicoRuntimeTests(unittest.TestCase):
    def config(self):
        config = types.ModuleType('config')
        source = Path(__file__).resolve().parents[2] / 'pico' / 'config.py'
        exec(compile(source.read_text(), str(source), 'exec'), config.__dict__)
        return config

    def runtime_path(self):
        return str(Path(__file__).resolve().parents[2] / 'pico' / 'main.py')

    def test_default_flags_block_runtime_before_hardware_import(self):
        config = self.config()
        for key in ('PINMAP_VERIFIED', 'POWER_AND_HARDWARE_STOP_VERIFIED',
                    'WHEEL_POLARITY_VERIFIED', 'ENABLE_ACTUATORS'):
            self.assertIs(getattr(config, key), False)
        with patch.dict(sys.modules, {'config': config}):
            with self.assertRaisesRegex(RuntimeError, 'Actuators disabled'):
                runpy.run_path(self.runtime_path())

    def test_serial_runtime_latches_stop_timeout_and_bad_json_with_fake_pwm(self):
        class EndRun(Exception):
            pass

        config = self.config()
        # Enable only this in-memory fixture; real config and hardware stay untouched.
        for key in ('PINMAP_VERIFIED', 'POWER_AND_HARDWARE_STOP_VERIFIED',
                    'WHEEL_POLARITY_VERIFIED', 'ENABLE_ACTUATORS'):
            setattr(config, key, True)
        active = dict(cmd='drive', armed=True, resume=True, vx=.5, vy=0, wz=0)
        ordinary = dict(active)
        del ordinary['resume']
        events = [(0, active), (100, dict(cmd='stop')), (200, ordinary),
                  (300, active), (701, ordinary), (800, active),
                  (900, '{bad json'), (1000, ordinary), (1100, active)]
        stream = io.StringIO()
        channels, history = [], []
        index = 0

        class Pin:
            OUT = 1
            def __init__(self, *args, **kwargs):
                pass

        class PWM:
            def __init__(self, pin, freq, duty_u16):
                self.value = duty_u16
                self.closed = False
                channels.append(self)
            def duty_u16(self, value):
                self.value = value
            def deinit(self):
                self.closed = True

        def ticks_ms():
            return events[index][0]

        def sleep_ms(delay):
            nonlocal index, stream
            history.append(tuple(channel.value for channel in channels))
            index += 1
            if index == len(events):
                raise EndRun()
            value = events[index][1]
            stream = io.StringIO((json.dumps(value) if isinstance(value, dict) else value) + '\n')

        class Input:
            def read(self, count):
                return stream.read(count)

        class Poll:
            def register(self, *args):
                pass
            def poll(self, timeout):
                return [(0, 1)] if stream.tell() < len(stream.getvalue()) else []

        machine = types.ModuleType('machine')
        machine.Pin, machine.PWM = Pin, PWM
        clock = types.ModuleType('time')
        clock.ticks_ms, clock.ticks_diff = ticks_ms, lambda current, previous: current-previous
        clock.sleep_ms = sleep_ms
        polling = types.ModuleType('uselect')
        polling.poll, polling.POLLIN = Poll, 1
        stream = io.StringIO(json.dumps(events[0][1]) + '\n')
        modules = dict(config=config, machine=machine, time=clock,
                       ujson=json, uselect=polling)
        with patch.dict(sys.modules, modules), patch.object(sys, 'stdin', Input()):
            with self.assertRaises(EndRun):
                runpy.run_path(self.runtime_path())
        self.assertEqual([any(values) for values in history],
                         [True, False, False, True, False, True, False, False, True])
        self.assertEqual(len(channels), 8)
        self.assertTrue(all(channel.closed and channel.value == 0 for channel in channels))


if __name__ == '__main__':
    unittest.main()
