from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtCore import Qt, QRectF, QPropertyAnimation, pyqtProperty
from PyQt5.QtGui import QPainter, QColor, QBrush

class ToggleSwitch(QCheckBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._position = 0.0
        self._animation = QPropertyAnimation(self, b"position", self)
        self._animation.setDuration(150)
        self.setFixedSize(36, 16)  # Nhỏ gọn
        self.setCursor(Qt.PointingHandCursor)
        self.toggled.connect(self.start_transition)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setChecked(not self.isChecked())

    def start_transition(self, checked):
        self._animation.stop()
        self._animation.setStartValue(self._position)
        self._animation.setEndValue(1.0 if checked else 0.0)
        self._animation.start()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        bg_rect = QRectF(0, 0, self.width(), self.height())
        bg_color = QColor("#2ecc71") if self.isChecked() else QColor("#777")
        p.setBrush(QBrush(bg_color))
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(bg_rect, self.height() / 2, self.height() / 2)

        margin = 2
        diameter = self.height() - margin * 2
        x = margin + (self.width() - diameter - margin * 2) * self._position
        circle_rect = QRectF(x, margin, diameter, diameter)
        p.setBrush(QBrush(Qt.white))
        p.drawEllipse(circle_rect)

    def get_position(self):
        return self._position

    def set_position(self, value):
        self._position = value
        self.update()

    position = pyqtProperty(float, fget=get_position, fset=set_position)
