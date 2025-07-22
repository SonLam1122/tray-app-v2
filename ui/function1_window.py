import time
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QRadioButton, QButtonGroup, QPushButton, QApplication, QTextEdit
)
from PyQt5.QtCore import Qt, QTimer
from util.util import move_to_bottom_right, back_to_main
from controllers.function1_controller import Function1Controller
import logic.funtion1_logic as logic
import pyperclip

class Function1Window(QWidget):
    def __init__(self, on_back):
        super().__init__()
        self.on_back = on_back
        self.controller = Function1Controller()
        self.selected_action = None
        self.last_clipboard = ""
        self._is_updating_ui = False

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.95)
        self.setFixedSize(260, 320)
        self.setStyleSheet("background-color: rgba(25, 25, 25, 230); border-radius: 6px;")

        self.init_ui()
        self.controller.bind_hotkeys(lambda: self.selected_action, self.update_status_display)

        self.clipboard_timer = QTimer(self)
        self.clipboard_timer.timeout.connect(self.check_clipboard)
        self.clipboard_timer.start(500)

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(6)

        title = QLabel("Function 1 (Radio)", self)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white; font-size: 11px; font-weight: bold;")
        main_layout.addWidget(title)

        # Radio buttons
        self.radio_group = QButtonGroup(self)
        radio_layout = QVBoxLayout()
        radio_layout.setSpacing(4)
        for action in self.controller.get_available_actions():
            btn = QRadioButton(action)
            btn.setStyleSheet(
                "QRadioButton {color: white; font-size: 12px; font-weight: 500; background: #232323; border-radius: 6px;}"
                "QRadioButton::indicator {width: 11px; height: 11px;}"
            )
            self.radio_group.addButton(btn)
            radio_layout.addWidget(btn)
            btn.toggled.connect(lambda checked, b=btn: self.on_action_selected_checked(b, checked))
        radio_widget = QWidget(self)
        radio_widget.setLayout(radio_layout)
        radio_widget.setStyleSheet("background: transparent; margin-bottom: 2px;")
        main_layout.addWidget(radio_widget, alignment=Qt.AlignCenter)

        # Key label
        self.key_label = QLabel("Key: None", self)
        self.key_label.setStyleSheet("color: #80ff80; font-size: 9.5px; margin-top: 1px;")
        main_layout.addWidget(self.key_label, alignment=Qt.AlignCenter)

        # OTP + countdown (ẩn mặc định)
        otp_row = QHBoxLayout()
        self.otp_label = QLabel("OTP: ------", self)
        self.otp_label.setStyleSheet("color: #ffd480; font-size: 15px; font-weight: bold; padding: 1px 6px; border-radius: 6px; background: #222;")
        otp_row.addStretch()
        otp_row.addWidget(self.otp_label)
        self.countdown_label = QLabel("", self)
        self.countdown_label.setStyleSheet("color: #80ff80; font-size: 11px; margin-left: 7px;")
        otp_row.addWidget(self.countdown_label)
        otp_row.addStretch()
        main_layout.addLayout(otp_row)
        self.otp_label.setVisible(False)
        self.countdown_label.setVisible(False)

        # Cookie display input (ẩn mặc định)
        self.cookie_input = QTextEdit(self)
        self.cookie_input.setStyleSheet(
            "color: #ffd480; font-size: 10px; background-color: #232323; border: 1px solid #444; border-radius: 6px; padding: 4px;"
        )
        self.cookie_input.setPlaceholderText("Cookies sẽ hiển thị ở đây...")
        self.cookie_input.setReadOnly(True)
        self.cookie_input.setFixedHeight(90)
        main_layout.addWidget(self.cookie_input)
        self.cookie_input.setVisible(False)

        main_layout.addStretch()

        # Back button
        btn_back = QPushButton("⟵ Quay lại")
        btn_back.setFixedSize(80, 26)
        btn_back.setStyleSheet(
            "QPushButton {color: white; font-size: 11px; background-color: #c0392b; border-radius: 8px;}"
            "QPushButton:hover {background-color: #e74c3c;}"
        )
        btn_back.clicked.connect(lambda: back_to_main(self))
        footer = QHBoxLayout()
        footer.addStretch()
        footer.addWidget(btn_back)
        main_layout.addLayout(footer)

        self.setFixedSize(260, 300)
        self.setStyleSheet("background-color: rgba(25, 25, 25, 230); border-radius: 6px;")
        move_to_bottom_right(self, position=15)

    def on_action_selected_checked(self, button, checked):
        if checked and button == self.radio_group.checkedButton():
            self.selected_action = button.text()
            print(f"🔘 Action selected: {self.selected_action}")

            # Ẩn tất cả các widget liên quan chức năng
            self.otp_label.setVisible(False)
            self.countdown_label.setVisible(False)
            self.cookie_input.setVisible(False)

            # Reset nền
            self.otp_label.setStyleSheet("color: #ffd480; font-size: 15px; font-weight: bold; padding: 1px 6px; border-radius: 6px; background: #222;")
            self.countdown_label.setStyleSheet("color: #80ff80; font-size: 11px; margin-left: 7px; background: #222; border-radius: 5px; padding: 2px 8px;")
            self.cookie_input.setStyleSheet("color: #ffd480; font-size: 10px; background-color: #232323; border: 1px solid #444; border-radius: 6px; padding: 4px;")

            # Hiện widget đúng với chức năng và thêm nền tối
            if self.selected_action == "Sinh mã OTP từ 2FA Key":
                self.otp_label.setVisible(True)
                self.countdown_label.setVisible(True)
                self.otp_label.setStyleSheet("color: white; font-size: 15px; font-weight: bold; padding: 1px 6px; border-radius: 6px; background: rgba(30,30,30,0.85);")
                self.countdown_label.setStyleSheet("color: white; font-size: 11px; margin-left: 7px; background: rgba(30,30,30,0.85); border-radius: 5px; padding: 2px 8px;")
            elif self.selected_action == "Convert Cookie sang JSON":
                self.cookie_input.setVisible(True)
                self.cookie_input.setStyleSheet("color: white; font-size: 11px; background-color: rgba(30,30,30,0.85); border: 1px solid #444; border-radius: 6px; padding: 4px;")

            self.check_clipboard(force=True)
            if self.selected_action == "Sinh mã OTP từ 2FA Key":
                if not hasattr(self, 'otp_timer'):
                    self.otp_timer = QTimer(self)
                    self.otp_timer.timeout.connect(self.update_otp_display)
                self.otp_timer.start(1000)
                self.update_otp_display()
            else:
                if hasattr(self, 'otp_timer'):
                    self.otp_timer.stop()

    def check_clipboard(self, force=False):
        try:
            clipboard = QApplication.clipboard()
            text = clipboard.text().strip()
            if text != self.last_clipboard or force:
                self.last_clipboard = text
                if self.selected_action == "Sinh mã OTP từ 2FA Key":
                    if self.controller.try_update_2fa_key(text):
                        logic.Current2FAKey = text
                        self.update_status_display()
                        return
                elif self.selected_action == "Convert Cookie sang JSON":
                    try:
                        logic.CurrentCookieJson = logic.convert_cookie_to_json(text)
                    except Exception:
                        logic.CurrentCookieJson = "[Lỗi chuyển cookie sang JSON]"
                self.update_status_display()
        except pyperclip.PyperclipException:
            pass

    def update_status_display(self):
        self._is_updating_ui = True
        self.key_label.setText(f"{logic.Current2FAKey or 'None'}")
        if self.selected_action == "Sinh mã OTP từ 2FA Key":
            self.update_otp_display()
        if self.selected_action == "Convert Cookie sang JSON":
            self.cookie_input.setPlainText(logic.CurrentCookieJson or "")
        self._is_updating_ui = False

    def update_otp_display(self):
        if logic.Current2FAKey:
            try:
                otp = logic.generate_totp(logic.Current2FAKey)
                self.otp_label.setText(f"OTP: {otp}")
                seconds = int(time.time())
                remain = 30 - (seconds % 30)
                self.countdown_label.setText(f"{remain:02d}s")
            except Exception:
                self.otp_label.setText("OTP: ------")
                self.countdown_label.setText("")
        else:
            self.otp_label.setText("OTP: ------")
            self.countdown_label.setText("")
