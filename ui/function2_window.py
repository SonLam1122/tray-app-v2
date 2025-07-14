from cProfile import label
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QTimer, QPoint

from controllers.function2_controller import Function2Controller
from logic.funtion2_logic import is_feature_enabled, set_feature_enabled
from util.util import move_to_bottom_right, back_to_main
from util.toggle_switch import ToggleSwitch

class Function2Window(QWidget):
    def __init__(self, on_back):
        super().__init__()
        self.on_back = on_back
        self.controller = Function2Controller()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.95)
        self.setFixedSize(260, 300)
        self.setStyleSheet("background-color: rgba(25, 25, 25, 230); border-radius: 6px;")

        self.init_ui()
        move_to_bottom_right(self, position=15)

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(6)

        title = QLabel("Function 2 (On/Off)", self)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white; font-size: 11px; font-weight: bold;")
        main_layout.addWidget(title)

        # Switch-like Checkboxes
        self.checkboxes = []
        for feature in self.controller.get_available_features():
            cb = ToggleSwitch()
            cb.setChecked(is_feature_enabled(feature))
            cb.stateChanged.connect(lambda state, f=feature: self.toggle_feature(f, state))
            self.checkboxes.append(cb)

            label = QLabel(feature)
            label.setStyleSheet("color: white; font-size: 10px;")

            row = QHBoxLayout()
            row.addWidget(label)
            row.addStretch()
            row.addWidget(cb)
            main_layout.addLayout(row)

        main_layout.addStretch()

        # Back button
        btn_back = QPushButton("Quay lại")
        btn_back.setFixedSize(80, 26)
        btn_back.setStyleSheet("""
            QPushButton {
                color: white;
                font-size: 10px;
                background-color: #c0392b;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #e74c3c;
            }
        """)
        btn_back.clicked.connect(lambda: back_to_main(self))

        footer = QHBoxLayout()
        footer.addStretch()
        footer.addWidget(btn_back)
        main_layout.addLayout(footer)

    def toggle_feature(self, feature, state):
        enabled = state == Qt.Checked
        set_feature_enabled(feature, enabled)
        print(f"{'Bật' if enabled else 'Tắt'} tính năng: {feature}")
        if enabled:
            self.controller.bind_feature(feature, None)

    def clear_feature_area(self):
        for i in reversed(range(self.feature_area_layout.count())):
            widget = self.feature_area_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

