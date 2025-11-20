# -*- coding: gbk -*-
import myactuator_rmd_py as rmd
import time
from myactuator_rmd_py.actuator_state import AccelerationType

# Initialization
driver = rmd.CanDriver("can2")
actuator = rmd.ActuatorInterface(driver, 3)

## Get initial acceleration
print(f"Initial acceleration: {actuator.getAcceleration()}")

actuator.setAcceleration(5000, AccelerationType.POSITION_PLANNING_ACCELERATION)

## Get modified acceleration
print(f"Modified acceleration: {actuator.getAcceleration()}")

# Set different acceleration types
actuator.setAcceleration(1000, AccelerationType.POSITION_PLANNING_ACCELERATION)
actuator.setAcceleration(800, AccelerationType.POSITION_PLANNING_DECELERATION)
actuator.setAcceleration(1200, AccelerationType.VELOCITY_PLANNING_ACCELERATION)
actuator.setAcceleration(1000, AccelerationType.VELOCITY_PLANNING_DECELERATION)
