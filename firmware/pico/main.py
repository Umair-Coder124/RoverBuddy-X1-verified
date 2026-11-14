"""Untested MicroPython drive starter, disabled by default.
Copy drive_logic.py, config.py and this file to a verified board only after review.
No autonomy, obstacle detection or servo control is implemented.
"""
import config

if not all((config.PINMAP_VERIFIED, config.POWER_AND_HARDWARE_STOP_VERIFIED,
            config.WHEEL_POLARITY_VERIFIED, config.ENABLE_ACTUATORS)):
    raise RuntimeError('Actuators disabled: hardware validation flags are false')

from machine import Pin, PWM
import sys, time
try:
    import ujson as json
    import uselect as select
except ImportError:
    import json, select
from drive_logic import DriveController

pairs = []
controller = DriveController()
def apply(values):
    for (a,b), value, sign in zip(pairs, values, config.MOTOR_SIGNS):
        # First set both low so a polarity change does not command both inputs high.
        a.duty_u16(0)
        b.duty_u16(0)
        value *= sign
        (a if value >= 0 else b).duty_u16(int(min(1,abs(value))*65535))

try:
    for ga,gb in config.MOTOR_PAIRS:
        a = PWM(Pin(ga,Pin.OUT,value=0), freq=config.PWM_HZ, duty_u16=0)
        b = PWM(Pin(gb,Pin.OUT,value=0), freq=config.PWM_HZ, duty_u16=0)
        pairs.append((a,b))
    poll = select.poll()
    poll.register(sys.stdin, select.POLLIN)
    previous = time.ticks_ms()
    elapsed = 0
    buffer = ''
    discard_line = False
    while True:
        tick = time.ticks_ms()
        elapsed += time.ticks_diff(tick, previous)
        previous = tick
        # Read bounded chunks without waiting for an entire line.
        for _ in range(128):
            if not poll.poll(0):
                break
            char = sys.stdin.read(1)
            if not char:
                controller.stop()
                break
            if char == '\n':
                if not discard_line:
                    try:
                        command = json.loads(buffer)
                        controller.receive(command, elapsed)
                    except (ValueError, TypeError):
                        controller.stop()
                buffer = ''
                discard_line = False
            elif not discard_line:
                if len(buffer) >= 256:
                    controller.stop()
                    buffer = ''
                    discard_line = True
                else:
                    buffer += char
        apply(controller.output(elapsed))
        time.sleep_ms(5)
finally:
    for a,b in pairs:
        a.duty_u16(0)
        b.duty_u16(0)
        a.deinit()
        b.deinit()
