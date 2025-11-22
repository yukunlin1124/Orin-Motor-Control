# -*- coding: utf-8 -*-
import os
import time
from motor_controller import MotorController
import numpy as np
from motor_logger import MotorFeedbackLogger
from Ankle.ankle import Ankle
from Cmd.poly345 import Poly345Cmd


def jointLinearInterpolation(initPos, targetPos, rate):

    rate = np.fmin(np.fmax(rate, 0.0), 1.0)
    p = initPos * (1 - rate) + targetPos * rate
    return p


if __name__ == "__main__":

    loop_time = 0.002  # seconds
    warmup_time = 1  # seconds
    duration_time = 10  # seconds
    cmd_period = 3  # seconds

    ankle_p_cmd = Poly345Cmd(20, -20, cmd_period)
    ankle_r_cmd = Poly345Cmd(5, -5, cmd_period)
    knee_cmd = Poly345Cmd(60, -60, cmd_period)

    q_cmd = [ankle_p_cmd, ankle_r_cmd, knee_cmd]
    q_init = [0.0, 0.0, 0.0]
    motor_cmd = [0.0, 0.0, 0.0]

    ankle_left = Ankle()

    motor1 = MotorController(can_port="can2", motor_id=1, torque_constant=2)
    motor2 = MotorController(can_port="can2", motor_id=2, torque_constant=2)
    motor3 = MotorController(can_port="can2", motor_id=3, torque_constant=2)
    motors = [motor1, motor2, motor3]

    log_file_base = "test2"
    log_filenames = [f"{log_file_base}_motor{i+1}.csv" for i in range(len(motors))]
    log_directory = os.path.join(os.path.dirname(__file__), "Datas")
    logger = MotorFeedbackLogger(
        file_path=log_directory, file_name=None, duration_time=duration_time
    )
    for motor in motors:
        motor.set_zero()
        motor.get_motor_status2()

    # User prompt
    print(
        "WARNING: Please ensure there are no obstacles around the robot while running this example."
    )
    input("Press Enter to continue...")

    try:
        start_time = time.time()
        t = 0.0
        while True:
            time.sleep(loop_time)
            t = time.time() - start_time

            if t >= 0:

                # first, go to initial joint position
                if t >= 0 and t < warmup_time:
                    motor_cmd[0], motor_cmd[1] = ankle_left.IK_deg(q_init[0], q_init[1])
                    motor_cmd[2] = q_init[2]

                # last, do poly345 motion
                if t >= warmup_time < duration_time:
                    phase_time = t - warmup_time
                    motor_cmd[0], motor_cmd[1] = ankle_left.IK_deg(
                        ankle_p_cmd.get(phase_time), ankle_r_cmd.get(phase_time)
                    )
                    motor_cmd[2] = knee_cmd.get(phase_time)

                if t >= duration_time:
                    for motor in motors:
                        motor.stop()
                        motor.shutdown()
                    break

                """
                cmd.motorCmd[d['FR_0']].q = qDes[0]
                cmd.motorCmd[d['FR_0']].dq = 0
                cmd.motorCmd[d['FR_0']].Kp = Kp[0]
                cmd.motorCmd[d['FR_0']].Kd = Kd[0]
                cmd.motorCmd[d['FR_0']].tau = -0.65
                """

            # safety shutdown after 30 seconds
            if t > 30:
                for motor in motors:
                    motor.stop()
                    motor.shutdown()
                break

            for motor, cmd in zip(motors, motor_cmd):
                motor.position_control(cmd, 120)

            # debug print
            # print(f"time: {t} s")

            # logger
            for motor, file_name in zip(motors, log_filenames):
                fb = motor.read_feedback()

                logger.log(
                    motor_id=motor.motor_id,
                    position=fb["position"],
                    velocity=fb["velocity"],
                    current=fb["current"],
                    temperature=fb["temperature"],
                    file_name=file_name,
                    log_time=t,
                )

    except KeyboardInterrupt:
        print("\nExiting interactive control...")
        for motor in motors:
            motor.stop()
            motor.shutdown()
