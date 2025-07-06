from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QRadioButton, QButtonGroup, QPushButton, QApplication
from PyQt5.QtCore import Qt, QTimer, QPoint
from controllers.function_controller import Function1Controller
import logic.funtion_logic as logic
import pyperclip

class FunctionWindow(QWidget):
    def __init__(self, on_back):
        super().__init__()
        self.on_back = on_back
        self.controller = Function1Controller()
        self.selected_action = None
        self.last_clipboard = ""

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.92)
        self.setFixedSize(240, 250)
        self.setStyleSheet("background-color: rgba(25, 25, 25, 230); border-radius: 6px;")

        self.init_ui()
        self.controller.bind_hotkeys(lambda: self.selected_action, self.update_status_display)

        self.clipboard_timer = QTimer(self)
        self.clipboard_timer.timeout.connect(self.check_clipboard)
        self.clipboard_timer.start(500)

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        title = QLabel("Tray App", self)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white; font-size: 11px; font-weight: bold;")
        layout.addWidget(title)

        self.radio_group = QButtonGroup(self)
        for action in self.controller.get_available_actions():
            btn = QRadioButton(action)
            btn.setStyleSheet("color: white; font-size: 9px;")
            self.radio_group.addButton(btn)
            layout.addWidget(btn)
            btn.toggled.connect(self.on_action_selected)

        self.key_label = QLabel("🔑 None", self)
        self.key_label.setStyleSheet("color: #80ff80; font-size: 9px;")
        layout.addWidget(self.key_label)

        self.buffer_label = QLabel("📋 (empty)", self)
        self.buffer_label.setStyleSheet("color: #ffd480; font-size: 9px;")
        self.buffer_label.setWordWrap(True)
        layout.addWidget(self.buffer_label)

        btn_quit = QPushButton("❌")
        btn_quit.setFixedSize(40, 24)
        btn_quit.setStyleSheet("color: white; font-size: 11px; background-color: #444; border-radius: 4px;")
        btn_quit.clicked.connect(QApplication.quit)

        footer = QHBoxLayout()
        footer.addStretch()
        footer.addWidget(btn_quit)
        layout.addLayout(footer)

        self.move_to_bottom_right()

    def on_action_selected(self):
        btn = self.radio_group.checkedButton()
        if btn and btn.isChecked():
            new_action = btn.text()
            if new_action != self.selected_action:
                self.selected_action = new_action
                print(f"🔘 Action selected: {new_action}")
                self.check_clipboard(force=True)

    def check_clipboard(self, force=False):
        text = pyperclip.paste().strip()
        if text != self.last_clipboard or force:
            self.last_clipboard = text
            self.handle_clipboard_update(text)
            self.update_status_display()

    def handle_clipboard_update(self, text):
        if not self.selected_action:
            return
        if self.selected_action == "Sinh mã OTP từ 2FA Key":
            self.controller.try_update_2fa_key(text)
        elif self.selected_action == "Dán từng phần chuỗi có dấu |" and "|" in text:
            self.controller.try_update_part_buffer(text)

    def update_status_display(self):
        self.key_label.setText(f"🔑 {logic.Current2FAKey or 'None'}")
        if logic.PartBuffer:
            lines = "\n".join(f"{i+1}. {p}" for i, p in enumerate(logic.PartBuffer))
            self.buffer_label.setText(f"📋\n{lines}")
        else:
            self.buffer_label.setText("📋 (empty)")

    def move_to_bottom_right(self):
        screen = self.screen().availableGeometry()
        x = screen.right() - self.width() - 10
        y = screen.bottom() - self.height() - 10
        self.move(QPoint(x, y))
