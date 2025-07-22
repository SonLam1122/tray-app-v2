from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, QApplication
from PyQt5.QtCore import Qt, QPoint, QTimer
import logic.funtion2_logic as logic2
import pyperclip

class PasteBufferWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.97)
        self.setFixedSize(260, 160)
        self._drag_active = False
        self._drag_position = QPoint()
        self.init_ui()
        self.update_panel()
        QTimer.singleShot(0, self.move_to_bottom_right)

        self.clipboard_timer = QTimer(self)
        self.clipboard_timer.timeout.connect(self.check_clipboard)
        self.clipboard_timer.start(500)

    def move_to_bottom_right(self):
        screen = self.screen() if hasattr(self, 'screen') else None
        if screen is None:
            screen = QApplication.primaryScreen()
        geometry = screen.availableGeometry() if screen else QApplication.desktop().availableGeometry()
        x = geometry.right() - self.width() - 20
        y = geometry.bottom() - self.height() - 40
        self.move(x, y)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_active = True
            self._drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._drag_active and event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self._drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_active = False
        event.accept()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(6)

        title = QLabel("Dán từng phần chuỗi có dấu |", self)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #ffd480; font-size: 12px; font-weight: bold;")
        layout.addWidget(title)

        index_layout = QHBoxLayout()
        index_label = QLabel("Index:", self)
        index_label.setStyleSheet("color: #ffd480; font-size: 10px;")
        self.index_input = QLineEdit(str(logic2.CurrentIndex), self)
        self.index_input.setStyleSheet("color: white; font-size: 10px; background-color: #333; border: 1px solid #555; border-radius: 3px; padding: 2px;")
        self.index_input.setFixedWidth(40)
        self.index_input.textChanged.connect(self.on_index_changed)
        index_layout.addWidget(index_label)
        index_layout.addWidget(self.index_input)
        index_layout.addStretch()
        layout.addLayout(index_layout)

        self.buffer_edit = QTextEdit(self)
        self.buffer_edit.setStyleSheet("color: #ffd480; font-size: 10px; background-color: #333; border-radius: 3px;")
        self.buffer_edit.setPlaceholderText("(empty buffer)")
        self.buffer_edit.textChanged.connect(self.on_buffer_edited)
        layout.addWidget(self.buffer_edit)

    def update_panel(self):
        self.index_input.setText(str(logic2.CurrentIndex))
        current_buffer_text = "\n".join(f"{i+1}. {line}" for i, line in enumerate(logic2.PartBuffer))
        if self.buffer_edit.toPlainText() != current_buffer_text:
            self.buffer_edit.setPlainText(current_buffer_text)

    def on_index_changed(self, text):
        if text and text.isdigit():
            logic2.CurrentIndex = int(text)

    def on_buffer_edited(self):
        text = self.buffer_edit.toPlainText()
        lines = [line.split('. ', 1)[1] if '. ' in line else line for line in text.split('\n') if line.strip()]
        logic2.PartBuffer[:] = lines 

    def check_clipboard(self):
        text = pyperclip.paste().strip()
        if text != logic2.LastValidClipboard and '|' in text:
            logic2.try_update_part_buffer(text)
            self.update_panel() 