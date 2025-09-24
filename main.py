import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from ttkbootstrap import Style

if __name__ == "__main__":
    app = QApplication(sys.argv)
    style = Style(theme="darkly")  # ttkbootstrap style
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
