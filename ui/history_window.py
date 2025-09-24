from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QScrollArea, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt
from ttkbootstrap import Style

class HistoryWindow(QDialog):
    def __init__(self, history, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Session History")
        self.setGeometry(100, 100, 550, 300)

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("History Log", alignment=Qt.AlignmentFlag.AlignCenter))

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        scroll_layout = QVBoxLayout()
        container.setLayout(scroll_layout)

        # Headers
        header = QHBoxLayout()
        for h, w in zip(["Date", "Table", "Start", "End", "Minutes"], [80, 80, 60, 60, 60]):
            lbl = QLabel(h)
            lbl.setFixedWidth(w)
            lbl.setStyleSheet("font-weight: bold;")
            header.addWidget(lbl)
        scroll_layout.addLayout(header)

        # Rows
        for row in reversed(history):
            row_layout = QHBoxLayout()
            for value, width in zip(row, [80, 80, 60, 60, 60]):
                lbl = QLabel(str(value))
                lbl.setFixedWidth(width)
                row_layout.addWidget(lbl)
            scroll_layout.addLayout(row_layout)

        scroll.setWidget(container)
        layout.addWidget(scroll)
