# All flags intentionally false. Review exact hardware before changing them.
PINMAP_VERIFIED = False
POWER_AND_HARDWARE_STOP_VERIFIED = False
WHEEL_POLARITY_VERIFIED = False
ENABLE_ACTUATORS = False

# Logical GPIO identifiers only; physical board pinout is unverified.
MOTOR_PAIRS = ((2,3), (4,5), (6,7), (8,9))  # FL, FR, RL, RR
MOTOR_SIGNS = (1,1,1,1)  # Calibrate each lifted wheel.
PWM_HZ = 1000
