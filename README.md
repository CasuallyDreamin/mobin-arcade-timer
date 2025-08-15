# Arcade Timer

A simple, minimal desktop application for tracking playtime at an arcade.  
Designed for quick, manual time tracking of multiple tables (billiards, bowling, consoles, PCs, etc.) without the complexity of real-time second tracking or automatic fee calculation.  

Built with **Python**, **Tkinter**, and **ttkbootstrap** for a modern dark-themed UI.

---

## Features

- Add and track multiple tables simultaneously.
- Start and stop timers with a single click.
- Automatically logs table name, start time, end time, and total minutes played.
- History log stored in a CSV file (`arcade_log.csv`).
- Displays most recent sessions first in the history viewer.
- Minimal, clean dark-themed interface.

---

## How It Works

1. Enter a **table name** in the input box and click **Add Table**.
2. The table is added to the **Active Timers** list with its start time.
3. When the session ends, click **Stop** — the total minutes are calculated and displayed.
4. The session is logged in both the **in-app history** and the CSV file.
5. Open the **History Log** to review all past sessions, with the most recent first.

---

## Running the App

1. Install Python 3.8+ and required dependencies:
   pip install ttkbootstrap

2. Run the app:
   python arcade_timer.py

---

## Building a Windows Executable

You can package the app into a standalone `.exe` using **PyInstaller**.

1. Install PyInstaller:
   pip install pyinstaller

2. Build the EXE:
   pyinstaller --onefile --windowed arcade_timer.py

3. Run the EXE:
   The executable will be located in `dist/arcade_timer.exe` and can be run directly.

---

## Files

- `arcade_timer.py` → Main application code
- `arcade_log.csv` → Generated log file storing session history (created automatically if missing)

---

