import csv
import os
import time


class MotorFeedbackLogger:
    def __init__(self,
                 file_path=".",
                 file_name="motor_feedback.csv",
                 duration_time=None):
        """
        Parameters
        ----------
        file_path : str
            Directory where the log file will be written.
        file_name : str
            Log file name.
        duration_time : float | None
            Optional experiment duration used for bookkeeping.
        """
        self.file_path = file_path or "."
        self.default_file_name = file_name
        self.duration_time = duration_time
        self.file_states = {}
        self.initialized_files = set()
        os.makedirs(self.file_path, exist_ok=True)
        if self.default_file_name:
            self._ensure_file_initialized(self.default_file_name)

    def _ensure_file_initialized(self, file_name):
        """
        Make sure the CSV exists with a header row.
        """
        full_path = os.path.join(self.file_path, file_name)
        if full_path in self.initialized_files:
            return full_path

        if not os.path.isfile(full_path):
            with open(full_path, mode="w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "time (s)",
                    "motor_id",
                    "position (deg)",
                    "velocity (rpm)",
                    "current (A)",
                    "temperature(C)"
                ])
        self.initialized_files.add(full_path)
        return full_path

    def _get_state(self, file_name):
        if file_name not in self.file_states:
            self.file_states[file_name] = {
                "elapsed_time": 0.0,
                "start_time": None
            }
        return self.file_states[file_name]

    def log(self,
            motor_id,
            position,
            velocity,
            current,
            temperature,
            file_name=None,
            log_time=None):
        target_file = file_name or self.default_file_name
        if not target_file:
            raise ValueError("A file_name must be provided either at init or during log().")

        full_path = self._ensure_file_initialized(target_file)
        state = self._get_state(target_file)

        if log_time is not None:
            elapsed_time = log_time
        else:
            now = time.time()
            if state["start_time"] is None:
                state["start_time"] = now
            elapsed_time = now - state["start_time"]

        # Clip elapsed time if duration_time provided
        if self.duration_time is not None:
            elapsed_time = min(elapsed_time, self.duration_time)

        with open(full_path, mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                elapsed_time,
                motor_id,
                position,
                velocity,
                current,
                temperature
            ])
