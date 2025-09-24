import csv
import os
from datetime import datetime

LOG_FILE = "arcade_log.csv"

class Logger:
    def __init__(self, file_path=LOG_FILE):
        self.file_path = file_path
        self.ensure_file()

    def ensure_file(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Date", "Table", "Start Time", "End Time", "Minutes"])

    def log(self, table_name, start, end, minutes):
        date_str = datetime.now().strftime("%Y-%m-%d")
        start_str = start.strftime("%H:%M")
        end_str = end.strftime("%H:%M")
        with open(self.file_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([date_str, table_name, start_str, end_str, minutes])

    def load_history(self):
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path) as f:
            reader = list(csv.reader(f))
            return reader[1:]  # skip header
