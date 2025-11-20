# -*- coding: gbk -*-
import myactuator_rmd_py as rmd
import time
driver = rmd.CanDriver("can2")
actuator = rmd.ActuatorInterface(driver, 3)

# Continuous rotation at 120 dps
actuator.sendVelocitySetpoint(120.0)
"""
time.sleep(15)

# Stop motor
actuator.stopMotor()
"""
# Get current position
angle = actuator.getMultiTurnAngle()
print(f"Current position: {angle} Degree")

mode = actuator.getControlMode()
print(f"Current control mode: {mode}")
