from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox,
    QScrollArea, QSizePolicy
)
from PyQt6.QtGui import QPixmap, QPainter, QIcon
from PyQt6.QtCore import QTimer, Qt
from core.timer_manager import TimerManager
from core.logger import Logger
from ui.history_window import HistoryWindow


# --- Transparent overlay class ---
class TransparentOverlay(QLabel):
    def __init__(self, parent, image_path, opacity=0.2):
        super().__init__(parent)
        self.image_path = image_path
        self.opacity = opacity

        # Let mouse/keyboard events pass through
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)

        self.update_overlay()
        self.show()

    def update_overlay(self):
        parent_size = self.parent().size()
        pixmap = QPixmap(self.image_path).scaled(
            parent_size,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )

        # Apply opacity
        overlay = QPixmap(pixmap.size())
        overlay.fill(Qt.GlobalColor.transparent)

        painter = QPainter(overlay)
        painter.setOpacity(self.opacity)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()

        self.setPixmap(overlay)
        self.setGeometry(self.parent().rect())


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TOOSKA")
        self.setWindowIcon(QIcon("arcade_icon.png"))
        self.setGeometry(100, 100, 600, 500)

        self.timer_manager = TimerManager()
        self.logger = Logger()
        self.timer_labels = {}  # {table_name: QLabel for elapsed time}

        # --- Global dark theme ---
        self.setStyleSheet("""
            QWidget {
                background-color: #1E1E1E;
                color: white;
                font-size: 14px;
            }
            QLineEdit {
                background-color: #2C2F33;
                color: white;
                border: 1px solid #3A3F44;
                border-radius: 4px;
                padding: 4px 8px;
            }
            QLabel {
                font-size: 14px;
            }
            QPushButton {
                padding: 6px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                filter: brightness(110%);
            }
        """)

        # Main vertical layout
        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.layout)

        self.init_top_frame()
        self.init_timer_area()

        # Overlay background image (arcade photo)
        self.overlay = TransparentOverlay(self, "arcade.png", opacity=0.15)

        # Live timer update
        self.update_timer = QTimer()
        self.update_timer.setInterval(1000)  # 1 second
        self.update_timer.timeout.connect(self.update_timer_labels)
        self.update_timer.start()

    # --- Resize event keeps overlay in sync ---
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "overlay"):
            self.overlay.update_overlay()

    # --- Top input and buttons ---
    def init_top_frame(self):
        top_frame = QHBoxLayout()
        top_frame.setSpacing(10)

        self.table_name_input = QLineEdit()
        self.table_name_input.setPlaceholderText("Enter table name")
        top_frame.addWidget(self.table_name_input)

        btn_add = QPushButton("Add Table")
        btn_add.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
            }
            QPushButton:hover {
                background-color: #3ac35a;
            }
        """)
        btn_add.clicked.connect(self.add_table)
        top_frame.addWidget(btn_add)

        btn_history = QPushButton("View History")
        btn_history.setStyleSheet("""
            QPushButton {
                background-color: #17a2b8;
                color: white;
            }
            QPushButton:hover {
                background-color: #20c6d4;
            }
        """)
        btn_history.clicked.connect(self.show_history)
        top_frame.addWidget(btn_history)

        self.layout.addLayout(top_frame)

    # --- Scrollable timers area ---
    def init_timer_area(self):
        # Scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()

        # Main vertical layout for scroll content
        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(5)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # force content to top
        self.scroll_widget.setLayout(self.scroll_layout)

        self.scroll_area.setWidget(self.scroll_widget)
        self.layout.addWidget(self.scroll_area)

        # Header
        self.header_widget = QWidget()
        self.header_widget.setFixedHeight(40)
        self.header_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.header_row = QHBoxLayout()
        self.header_row.setContentsMargins(0, 0, 0, 0)
        self.header_row.setSpacing(5)
        self.header_widget.setLayout(self.header_row)

        for h, w in zip(["Table Name", "Elapsed Time", "Action"], [250, 120, 120]):
            lbl = QLabel(h)
            lbl.setFixedWidth(w)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet(
                "font-weight: bold; background-color: #2C2F33; color: #FFFFFF; "
                "padding: 4px; border-bottom: 2px solid #3A9AD9;"
            )
            self.header_row.addWidget(lbl)

        self.scroll_layout.addWidget(self.header_widget)

    # --- Add table ---
    def add_table(self):
        name = self.table_name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Warning", "Please enter a table name.")
            return
        try:
            self.timer_manager.add_timer(name)
        except ValueError:
            QMessageBox.warning(self, "Warning", "That table already exists.")
            return
        self.table_name_input.clear()
        self.refresh_timers()

    # --- Stop table timer ---
    def stop_table(self, name):
        result = self.timer_manager.stop_timer(name)
        if result:
            start, end, minutes = result
            self.logger.log(name, start, end, minutes)

            # Convert to hours + minutes
            hours, mins = divmod(minutes, 60)
            time_str = f"{hours}h {mins}m" if hours > 0 else f"{mins}m"

            QMessageBox.information(
                self,
                "Session Ended",
                f"Table '{name}' played for {time_str}."
            )
            self.refresh_timers()

    # --- Show history ---
    def show_history(self):
        history = self.logger.load_history()
        dlg = HistoryWindow(history, self)
        dlg.exec()

    # --- Refresh timers ---
    def refresh_timers(self):
        # Remove all rows except the header
        for i in reversed(range(1, self.scroll_layout.count())):  # skip header at index 0
            item = self.scroll_layout.itemAt(i)
            if item is None:
                continue
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()

        self.timer_labels.clear()

        # Add active timers
        for index, (name, start) in enumerate(self.timer_manager.get_active_timers().items()):
            row_widget = QWidget()
            row_widget.setFixedHeight(40)  # same height as header
            row_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

            row_layout = QHBoxLayout()
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(5)
            row_widget.setLayout(row_layout)

            # Zebra stripes
            bg_color = "#2C2F33" if index % 2 == 0 else "#23272A"
            row_widget.setStyleSheet(f"""
                QWidget {{
                    background-color: {bg_color};
                    border-radius: 4px;
                }}
                QWidget:hover {{
                    background-color: #3A3F44;
                }}
            """)

            lbl_name = QLabel(name)
            lbl_name.setFixedWidth(250)
            lbl_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
            row_layout.addWidget(lbl_name)

            elapsed_lbl = QLabel("00:00")
            elapsed_lbl.setFixedWidth(120)
            elapsed_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            elapsed_lbl.setStyleSheet("font-family: Consolas, monospace;")
            row_layout.addWidget(elapsed_lbl)
            self.timer_labels[name] = elapsed_lbl

            btn_stop = QPushButton("Stop")
            btn_stop.setFixedWidth(120)
            btn_stop.setStyleSheet("""
                QPushButton {
                    background-color: #D9534F;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #e36864;
                }
            """)
            btn_stop.clicked.connect(lambda _, n=name: self.stop_table(n))
            row_layout.addWidget(btn_stop)

            self.scroll_layout.addWidget(row_widget)

    # --- Update elapsed timers ---
    def update_timer_labels(self):
        from datetime import datetime
        for name, start in self.timer_manager.get_active_timers().items():
            elapsed = datetime.now() - start
            hours, remainder = divmod(int(elapsed.total_seconds()), 3600)
            minutes = remainder // 60
            if name in self.timer_labels:
                self.timer_labels[name].setText(f"{hours:02d}:{minutes:02d}")
