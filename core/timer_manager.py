from datetime import datetime

class TimerManager:
    def __init__(self):
        self.timers = {}

    def add_timer(self, table_name):
        if table_name in self.timers:
            raise ValueError("Table already exists")
        self.timers[table_name] = datetime.now()

    def stop_timer(self, table_name):
        start_time = self.timers.pop(table_name, None)
        if start_time:
            end_time = datetime.now()
            minutes = int((end_time - start_time).total_seconds() // 60)
            return start_time, end_time, minutes
        return None

    def get_active_timers(self):
        return self.timers.copy()
