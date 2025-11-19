import csv
import os
import time

class MotorFeedbackLogger:
    def __init__(self, filename="motor_feedback.csv"):
        self.filename = filename

        # Create file with header if not exists
        if not os.path.isfile(self.filename):
            with open(self.filename, mode="w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "timestamp",
                    "motor_id",
                    "position_deg",
                    "velocity_rpm",
                    "current_A",
                    "temperature_C"
                ])

    def log(self, motor_id, position, velocity, current, temperature):
        with open(self.filename, mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                time.time(),
                motor_id,
                position,
                velocity,
                current,
                temperature
            ])
