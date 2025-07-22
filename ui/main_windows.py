from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QApplication
from PyQt5.QtCore import Qt
import sys

from ui.function2_window import Function2Window
from ui.function1_window import Function1Window
from util.util import move_to_bottom_right

class MiniTrayWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Cài đặt cửa sổ
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.96)
        self.setFixedSize(200, 148)
        self.setStyleSheet("""
            background-color: qlineargradient(
                spread:pad, x1:0, y1:0, x2:1, y2:1,
                stop:0 rgba(35, 35, 35, 250),
                stop:1 rgba(25, 25, 25, 240)
            );
            border-radius: 10px;
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(6)

        # Tạo các nút
        buttons = [
            ("Function 1", self.on_func1),
            ("Function 2", self.on_func2),
            ("Settings", self.on_settings),
            ("Exit", QApplication.quit)
        ]

        for text, handler in buttons:
            btn = QPushButton(text)
            btn.setFixedHeight(30)
            btn.setStyleSheet("""
                QPushButton {
                    color: #f0f0f0;
                    font-size: 10.5px;
                    font-weight: 500;
                    background-color: #2c2c2c;
                    border: 1px solid #3a3a3a;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #3d3d3d;
                    border: 1px solid #5c5c5c;
                }
            """)
            btn.clicked.connect(handler)
            layout.addWidget(btn)

    def showEvent(self, event):
        super().showEvent(event)
        move_to_bottom_right(self, position=10)

    def on_func1(self):
        if not hasattr(self, 'function1_window') or self.function1_window is None:
            self.function1_window = Function1Window(on_back=self.show)
            # Reset biến khi cửa sổ bị đóng
            self.function1_window.destroyed.connect(lambda: setattr(self, 'function1_window', None))
            
        self.hide()
        self.function1_window.show()
        self.function1_window.raise_()
        self.function1_window.activateWindow()

    def on_func2(self):
        if not hasattr(self, 'function2_window') or self.function2_window is None:
            self.function2_window = Function2Window(on_back=self.show)
            # Reset biến khi cửa sổ bị đóng
            self.function2_window.destroyed.connect(lambda: setattr(self, 'function2_window', None))

        self.hide()
        self.function2_window.show()
        self.function2_window.raise_()
        self.function2_window.activateWindow()

    def on_settings(self):
        print("Settings clicked")