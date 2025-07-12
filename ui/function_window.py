from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QRadioButton, QButtonGroup, QPushButton, QApplication, QLineEdit, QTextEdit
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QIntValidator
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
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(8)

        title = QLabel("Tray App", self)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white; font-size: 12px; font-weight: bold;")
        main_layout.addWidget(title)

        self.radio_group = QButtonGroup(self)
        for action in self.controller.get_available_actions():
            btn = QRadioButton(action)
            btn.setStyleSheet("color: white; font-size: 10px;")
            self.radio_group.addButton(btn)
            main_layout.addWidget(btn)
            btn.toggled.connect(self.on_action_selected)

        self.key_label = QLabel("🔑 None", self)
        self.key_label.setStyleSheet("color: #80ff80; font-size: 10px;")
        main_layout.addWidget(self.key_label)

        self.paste_widget = QWidget(self)
        paste_layout = QVBoxLayout(self.paste_widget)
        paste_layout.setContentsMargins(0, 5, 0, 5)

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

        btn_quit = QPushButton("❌")
        btn_quit.setFixedSize(60, 26)
        btn_quit.setStyleSheet("color: white; font-size: 11px; background-color: #c0392b; border-radius: 4px;")
        btn_quit.clicked.connect(QApplication.quit)
        
        footer = QHBoxLayout()
        footer.addStretch()
        footer.addWidget(btn_quit)
        main_layout.addLayout(footer)

        self.paste_widget.setVisible(False)
        self.move_to_bottom_right()
        
    def on_action_selected(self):
        btn = self.radio_group.checkedButton()
        if btn and btn.isChecked():
            self.selected_action = btn.text()
            print(f"🔘 Action selected: {self.selected_action}")
            is_paste_action = self.selected_action == "Dán từng phần chuỗi có dấu |"
            self.paste_widget.setVisible(is_paste_action)
            self.key_label.setVisible(not is_paste_action)
            self.check_clipboard(force=True)

    def on_index_changed(self, text):
        if text and text.isdigit():
            logic.CurrentIndex = int(text)

    def on_buffer_edited(self):
        if not self._is_updating_ui:
            text = self.buffer_edit.toPlainText()
            logic.PartBuffer[:] = [line.strip() for line in text.split('\n') if line.strip()]

    def check_clipboard(self, force=False):
        try:
            text = pyperclip.paste().strip()
            if text != self.last_clipboard or force:
                self.last_clipboard = text
                if self.selected_action == "Dán từng phần chuỗi có dấu |" and "|" in text:
                    if text != logic.LastValidClipboard:
                        self.controller.try_update_part_buffer(text)
                # Gọi update_status_display sau khi clipboard thay đổi
                self.update_status_display()
        except pyperclip.PyperclipException:
            pass

    def update_status_display(self):
        self._is_updating_ui = True
        
        self.key_label.setText(f"🔑 {logic.Current2FAKey or 'None'}")
        
        current_buffer_text = "\n".join(logic.PartBuffer)
        if self.buffer_edit.toPlainText() != current_buffer_text:
            self.buffer_edit.setPlainText(current_buffer_text)
            
        # Cập nhật ô nhập chỉ mục để phản ánh thay đổi từ logic
        if self.index_input.text() != str(logic.CurrentIndex):
            self.index_input.setText(str(logic.CurrentIndex))
            
        self._is_updating_ui = False

    def move_to_bottom_right(self):
        screen = QApplication.primaryScreen().availableGeometry()
        x = screen.right() - self.width() - 15
        y = screen.bottom() - self.height() - 15
        self.move(QPoint(x, y))