# -*- coding: gbk -*-
import myactuator_rmd_py as rmd
import time
driver = rmd.CanDriver("can2")
actuator = rmd.ActuatorInterface(driver, 3)

# Move to 180 degree position at 100 deg/s
actuator.sendPositionAbsoluteSetpoint(180, 100.0)
time.sleep(10)  # Wait for motor to reach target position

# Get current position
angle = actuator.getMultiTurnAngle()
print(f"Current position: {angle} Degree")

time.sleep(5)
mode = actuator.getControlMode()
print(f"Current control mode: {mode}")
actuator.shutdownMotor()
