# -*- coding: gbk -*-
import myactuator_rmd_py as rmd
import time
driver = rmd.CanDriver("can2")
actuator = rmd.ActuatorInterface(driver, 3)

# Apply 0.5A current (torque)
actuator.sendCurrentSetpoint(0.5)
time.sleep(2)

# Stop torque output
actuator.stopMotor()

# Get current position
angle = actuator.getMultiTurnAngle()
print(f"Current position: {angle} Degree")

mode = actuator.getControlMode()
print(f"Current control mode: {mode}")
