# Leave these off until an adult has checked the hardware.
PINMAP_VERIFIED = False
POWER_AND_HARDWARE_STOP_VERIFIED = False
WHEEL_POLARITY_VERIFIED = False
ENABLE_ACTUATORS = False

# Proposed GPIO numbers. Check the real board first.
MOTOR_PAIRS = ((2, 3), (4, 5), (6, 7), (8, 9))  # FL, FR, RL, RR
MOTOR_SIGNS = (1, 1, 1, 1)  # Calibrate each lifted wheel.
PWM_HZ = 1000
