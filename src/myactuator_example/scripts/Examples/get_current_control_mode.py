# -*- coding: gbk -*-
import myactuator_rmd_py as rmd
import time
driver = rmd.CanDriver("can2")
actuator = rmd.ActuatorInterface(driver, 3)
mode = actuator.getControlMode()
print(f"Current Control Mode: {mode}")
