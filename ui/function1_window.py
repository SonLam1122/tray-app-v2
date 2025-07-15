from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QRadioButton, QButtonGroup, QPushButton, QApplication, QLineEdit, QTextEdit
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIntValidator
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
        for action in self.controller.get_available_actions():
            btn = QRadioButton(action)
            btn.setStyleSheet("""
                QRadioButton {
                    color: white;
                    font-size: 9.5px;
                    padding: 2px;
                }
                QRadioButton::indicator {
                    width: 10px;
                    height: 10px;
                }
            """)
            self.radio_group.addButton(btn)
            main_layout.addWidget(btn)
            btn.toggled.connect(lambda checked, b=btn: self.on_action_selected_checked(b, checked))

        # Key label
        self.key_label = QLabel("Key: None", self)
        self.key_label.setStyleSheet("color: #80ff80; font-size: 9.5px;")
        main_layout.addWidget(self.key_label)

        # Paste block
        self.paste_widget = QWidget(self)
        paste_layout = QVBoxLayout(self.paste_widget)
        paste_layout.setContentsMargins(0, 5, 0, 5)
        paste_layout.setSpacing(4)

        index_layout = QHBoxLayout()
        index_label = QLabel("Index:", self)
        index_label.setStyleSheet("color: #ffd480; font-size: 10px;")
        self.index_input = QLineEdit(str(logic.CurrentIndex), self)
        self.index_input.setValidator(QIntValidator(1, 10))
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
        
        main_layout.addWidget(self.paste_widget)
        main_layout.addStretch()

        # Cookie display input
        self.cookie_input = QTextEdit(self)
        self.cookie_input.setStyleSheet("""
            color: #ffd480;
            font-size: 10px;
            background-color: #333;
            border: 1px solid #555;
            border-radius: 3px;
            padding: 4px;
        """)
        self.cookie_input.setPlaceholderText("Cookies sẽ hiển thị ở đây...")
        self.cookie_input.setReadOnly(True)
        self.cookie_input.setFixedHeight(185) 
        main_layout.addWidget(self.cookie_input)
        self.cookie_input.setVisible(False)
        
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

        self.paste_widget.setVisible(False)
        move_to_bottom_right(self, position=15)

    def on_action_selected_checked(self, button, checked):
        if checked and button == self.radio_group.checkedButton():
            self.selected_action = button.text()
            print(f"🔘 Action selected: {self.selected_action}")

            is_paste_action = self.selected_action == "Dán từng phần chuỗi có dấu |"
            is_cookie_action = self.selected_action == "Convert Cookie sang JSON"

            self.paste_widget.setVisible(is_paste_action)
            self.cookie_input.setVisible(is_cookie_action)
            self.key_label.setVisible(not is_paste_action and not is_cookie_action)

            self.check_clipboard(force=True)


    def on_index_changed(self, text):
        if text and text.isdigit():
            logic.CurrentIndex = int(text)

    def on_buffer_edited(self):
        if not self._is_updating_ui:
            text = self.buffer_edit.toPlainText()
            lines = [line.split('. ', 1)[1] if '. ' in line else line for line in text.split('\n') if line.strip()]
            logic.PartBuffer[:] = lines

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
                
                elif self.selected_action == "Dán từng phần chuỗi có dấu |" and "|" in text:
                    if text != logic.LastValidClipboard:
                        self.controller.try_update_part_buffer(text)

                elif self.selected_action == "Convert Cookie sang JSON":
                    try:
                        logic.CurrentCookieJson = logic.convert_cookie_to_json(text)
                    except Exception as e:
                        logic.CurrentCookieJson = "[Lỗi chuyển cookie sang JSON]"
                
                self.update_status_display()

        except pyperclip.PyperclipException:
            pass

    def update_status_display(self):
        self._is_updating_ui = True

        self.key_label.setText(f"{logic.Current2FAKey or 'None'}")

        current_buffer_text = "\n".join(f"{i+1}. {line}" for i, line in enumerate(logic.PartBuffer))
        if self.buffer_edit.toPlainText() != current_buffer_text:
            self.buffer_edit.setPlainText(current_buffer_text)

        if self.index_input.text() != str(logic.CurrentIndex):
            self.index_input.setText(str(logic.CurrentIndex))
        
        if hasattr(self, 'cookie_input'):
            self.cookie_input.setPlainText(logic.CurrentCookieJson or "")

        self._is_updating_ui = False
