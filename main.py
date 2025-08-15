# arcade_timer.py
import tkinter as tk
from datetime import datetime
import csv
import os
import ttkbootstrap as tb
from ttkbootstrap.constants import *

LOG_FILE = "arcade_log.csv"

class ArcadeTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mobin's timer")
        self.root.geometry("500x400")
        
        self.timers = {}  # {table_name: start_time}
        self.history = []  # session history in memory

        # --- Top frame: label, input, and button ---
        top_frame = tb.Frame(root, padding=10)
        top_frame.pack(fill=X)

        lbl_table = tb.Label(top_frame, text="Table Name:", font=("Segoe UI", 10, "bold"))
        lbl_table.pack(anchor="w")

        self.table_name_var = tk.StringVar()
        self.entry_table = tb.Entry(top_frame, textvariable=self.table_name_var, width=30)
        self.entry_table.pack(side=LEFT, padx=(0, 10), pady=(2, 0))

        btn_add = tb.Button(top_frame, text="Add Table", bootstyle=SUCCESS, command=self.add_table)
        btn_add.pack(side=LEFT, pady=(2, 0))

        btn_history = tb.Button(top_frame, text="View History", bootstyle=INFO, command=self.show_history)
        btn_history.pack(side=LEFT, padx=(10, 0), pady=(2, 0))

        # --- Active timers frame ---
        self.timers_frame = tb.Frame(root, padding=10)
        self.timers_frame.pack(fill=BOTH, expand=True)

        # Ensure log file exists
        if not os.path.exists(LOG_FILE):
            with open(LOG_FILE, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Table", "Start Time", "End Time", "Minutes"])

    def add_table(self):
        name = self.table_name_var.get().strip()
        if not name:
            tb.dialogs.Messagebox.show_warning("Please enter a table name.", "Warning")
            return
        if name in self.timers:
            tb.dialogs.Messagebox.show_warning("That table already exists.", "Warning")
            return
        
        self.timers[name] = datetime.now()
        self.table_name_var.set("")
        self.refresh_timers()

    def stop_table(self, name):
        start_time = self.timers.pop(name, None)
        if start_time:
            end_time = datetime.now()
            elapsed_minutes = int((end_time - start_time).total_seconds() // 60)
            self.log_session(name, start_time, end_time, elapsed_minutes)
            tb.dialogs.Messagebox.ok(
                f"Table '{name}' played for {elapsed_minutes} minutes.",
                title="Session Ended",
                alert=True,
            )
            self.refresh_timers()

    def log_session(self, name, start_time, end_time, minutes):
        date_str = datetime.now().strftime("%Y-%m-%d")
        start_str = start_time.strftime("%H:%M")
        end_str = end_time.strftime("%H:%M")
        self.history.append((date_str, name, start_str, end_str, minutes))
        
        with open(LOG_FILE, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([date_str, name, start_str, end_str, minutes])

    def show_history(self):
        # Load history from file
        history = []
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, mode="r") as file:
                reader = list(csv.reader(file))
                history = reader[1:]  # skip header

        hist_win = tb.Toplevel(self.root)
        hist_win.title("Session History")
        hist_win.geometry("550x300")

        tb.Label(hist_win, text="History Log", bootstyle="inverse-info").pack(fill=X)

        # Column headers for history
        header_frame = tb.Frame(hist_win)
        header_frame.pack(fill=X)
        tb.Label(header_frame, text="Date", width=12, bootstyle="info").pack(side=LEFT)
        tb.Label(header_frame, text="Table", width=12, bootstyle="info").pack(side=LEFT)
        tb.Label(header_frame, text="Start", width=8, bootstyle="info").pack(side=LEFT)
        tb.Label(header_frame, text="End", width=8, bootstyle="info").pack(side=LEFT)
        tb.Label(header_frame, text="Minutes", width=8, bootstyle="info").pack(side=LEFT)
        # Vertical scrollbar
        scroll_y = tk.Scrollbar(hist_win, orient="vertical")
        scroll_y.pack(side=RIGHT, fill=Y)

        # Text area with vertical scroll
        text_area = tk.Text(hist_win, wrap="none", height=15, font=("Consolas", 10),
                            yscrollcommand=scroll_y.set)
        text_area.pack(fill=BOTH, expand=True)

        scroll_y.config(command=text_area.yview)

        for row in reversed(history):
            text_area.insert(tk.END, f"{row[0]:<12} {row[1]:<12} {row[2]:<8} {row[3]:<8} {row[4]} min\n")

        text_area.config(state="disabled")

    def refresh_timers(self):
        for widget in self.timers_frame.winfo_children():
            widget.destroy()

        # Active timers title
        tb.Label(self.timers_frame, text="Active Timers", bootstyle="inverse-secondary", anchor="center").pack(fill=X, pady=(0, 5))

        # Column headers for active timers
        header_frame = tb.Frame(self.timers_frame)
        header_frame.pack(fill=X)
        tb.Label(header_frame, text="Table Name", width=20, bootstyle="info").pack(side=LEFT)
        tb.Label(header_frame, text="Start Time", width=15, bootstyle="info").pack(side=LEFT)
        tb.Label(header_frame, text="Action", width=10, bootstyle="info").pack(side=LEFT)

        # Timer rows
        for name, start_time in self.timers.items():
            frame = tb.Frame(self.timers_frame)
            frame.pack(fill=X, pady=2)

            tb.Label(frame, text=name, width=20).pack(side=LEFT)
            tb.Label(frame, text=start_time.strftime("%H:%M"), width=15).pack(side=LEFT)

            btn_stop = tb.Button(frame, text="Stop", bootstyle=DANGER, command=lambda n=name: self.stop_table(n))
            btn_stop.pack(side=LEFT, padx=5)

if __name__ == "__main__":
    app = tb.Window(themename="darkly")
    ArcadeTimerApp(app)
    app.mainloop()
