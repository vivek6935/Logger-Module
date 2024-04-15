import os
import threading
import time
from datetime import datetime
import inspect

class Logger:
    def __init__(self, log_file='log.txt', log_level='INFO'):
        self.log_file = log_file
        self.log_level = log_level
        self.lock = threading.Lock()
        self.rotation_threshold = 10000  # 10 KB
        self.rotation_count = 10

        # Create log file directory if not exists
        log_dir = os.path.dirname(log_file)
        os.makedirs(log_dir, exist_ok=True)

        # Create log file if not exists
        if not os.path.exists(log_file):
            with open(log_file, 'w') as f:
                f.write('')

    def log(self, message, level='INFO'):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # Remove microseconds
        thread_id = threading.get_ident()
        caller_frame = self._get_caller_frame()
        if caller_frame:
            filename = os.path.basename(caller_frame.f_code.co_filename)
            function = caller_frame.f_code.co_name
        else:
            filename = ""
            function = ""

        # Check if the provided log level is valid
        if level not in {'DEBUG', 'INFO', 'ERROR'}:
            raise ValueError(f"Invalid log level '{level}'. Valid log levels are: DEBUG, INFO, ERROR")

        log_entry = f"{timestamp} | {level} | {filename} | {function} | Thread-{thread_id} | {message}\n"

        with self.lock:
            self._rotate_log_file_if_needed()
            with open(self.log_file, 'a') as f:
                f.write(log_entry)


    def _rotate_log_file_if_needed(self):
        current_size = os.path.getsize(self.log_file)
        if current_size > self.rotation_threshold:
            for i in range(self.rotation_count - 1, 0, -1):
                old_file = f"{self.log_file}.{i}"
                if os.path.exists(old_file):
                    os.remove(old_file)
            for i in range(self.rotation_count - 1, 0, -1):
                old_file = f"{self.log_file}.{i}"
                new_file = f"{self.log_file}.{i+1}"
                if os.path.exists(old_file):
                    os.rename(old_file, new_file)
            os.rename(self.log_file, f"{self.log_file}.1")
            with open(self.log_file, 'w') as f:
                pass

    def _get_caller_frame(self):
        # Get caller frame excluding Logger methods
        frames = inspect.stack()
        for frame_info in frames[2:]:
            frame = frame_info.frame
            if os.path.basename(frame.f_code.co_filename) != 'logger.py' and frame.f_code.co_name != '__init__':
                return frame
        # If caller frame is not found, print a warning and return None
        print("Warning: Could not retrieve caller frame.")
        return None
