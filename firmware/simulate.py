"""Run on a desktop: python3 firmware/simulate.py"""
from drive_logic import DriveController
controller = DriveController()
controller.receive({'cmd':'drive','armed':True,'vx':0.5,'vy':0,'wz':0.1}, 0)
print('Simulated FL/FR/RL/RR at 0 ms:', controller.output(0))
print('After command timeout at 401 ms:', controller.output(401))
print('Simulation only. No motors or hardware were accessed.')
