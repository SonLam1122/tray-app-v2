from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTextEdit
from PyQt5.QtCore import Qt

from controllers.function2_controller import Function2Controller
from logic.funtion2_logic import is_feature_enabled, set_feature_enabled
from util.util import move_to_bottom_right, back_to_main
from util.toggle_switch import ToggleSwitch
from ui.paste_buffer_window import PasteBufferWindow

from logic import funtion2_logic as logic2
import pyperclip
from logic.funtion2_logic import try_update_part_buffer, LastValidClipboard

class Function2Window(QWidget):
    def __init__(self, on_back):
        super().__init__()
        self.on_back = on_back
        self.controller = Function2Controller()
        self.paste_buffer_window = None

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

        # Panel dán từng phần chuỗi có dấu |
        self.paste_panel = QWidget(self)
        paste_layout = QVBoxLayout(self.paste_panel)
        paste_layout.setContentsMargins(0, 5, 0, 5)
        paste_layout.setSpacing(4)

        index_layout = QHBoxLayout()
        index_label = QLabel("Index:", self)
        index_label.setStyleSheet("color: #ffd480; font-size: 10px;")
        from logic import funtion2_logic as logic2
        self.index_input = QLineEdit(str(logic2.CurrentIndex), self)
        self.index_input.setStyleSheet("color: white; font-size: 10px; background-color: #333; border: 1px solid #555; border-radius: 3px; padding: 2px;")
        self.index_input.setFixedWidth(40)
        self.index_input.textChanged.connect(self.on_index_changed)
        index_layout.addWidget(index_label)
        index_layout.addWidget(self.index_input)
        index_layout.addStretch()
        paste_layout.addLayout(index_layout)

        self.buffer_edit = QTextEdit(self)
        self.buffer_edit.setStyleSheet("color: #ffd480; font-size: 10px; background-color: #333; border-radius: 3px;")
        self.buffer_edit.setPlaceholderText("(empty buffer)")
        self.buffer_edit.textChanged.connect(self.on_buffer_edited)
        paste_layout.addWidget(self.buffer_edit)

        main_layout.addWidget(self.paste_panel)
        self.paste_panel.setVisible(False)

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
        else:
            self.controller.unbind_feature(feature)

        # Nếu là Dán từng phần chuỗi có dấu | thì show/hide cửa sổ nổi
        if feature == "Dán từng phần chuỗi có dấu |":
            if enabled:
                if not self.paste_buffer_window:
                    self.paste_buffer_window = PasteBufferWindow()
                self.paste_buffer_window.show()
                self.paste_buffer_window.raise_()
                self.paste_buffer_window.activateWindow()
            else:
                if self.paste_buffer_window:
                    self.paste_buffer_window.close()
                    self.paste_buffer_window = None

    def on_index_changed(self, text):
        if text and text.isdigit():
            logic2.CurrentIndex = int(text)

    def on_buffer_edited(self):
        text = self.buffer_edit.toPlainText()
        lines = [line.split('. ', 1)[1] if '. ' in line else line for line in text.split('\n') if line.strip()]
        logic2.PartBuffer[:] = lines

    def update_paste_panel(self):
        # Cập nhật index và buffer từ logic
        self.index_input.setText(str(logic2.CurrentIndex))
        current_buffer_text = "\n".join(f"{i+1}. {line}" for i, line in enumerate(logic2.PartBuffer))
        if self.buffer_edit.toPlainText() != current_buffer_text:
            self.buffer_edit.setPlainText(current_buffer_text)

    def check_clipboard(self):
        
        try:
            text = pyperclip.paste().strip()
            if text != LastValidClipboard and '|' in text:
                try_update_part_buffer(text)
                self.update_paste_panel()
        except Exception:
            pass

    def clear_feature_area(self):
        for i in reversed(range(self.feature_area_layout.count())):
            widget = self.feature_area_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

