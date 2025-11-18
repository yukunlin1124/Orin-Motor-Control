# -*- coding: gbk -*-
import myactuator_rmd_py as rmd
import time
driver = rmd.CanDriver("can2")
actuator = rmd.ActuatorInterface(driver, 3)
actuator.setCurrentPositionAsEncoderZero()
actuator.reset()
time.sleep(1)
driver = rmd.CanDriver("can2")
actuator = rmd.ActuatorInterface(driver, 3)
print("Current position set as encoder zero point")
new_pos = actuator.getMultiTurnEncoderPosition()
print(f"Post-reboot position (should be near 0): {new_pos}")
