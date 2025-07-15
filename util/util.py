from PyQt5.QtCore import QPoint
from logic.funtion2_logic import human_type_handler, is_feature_enabled
import keyboard

# chuyển cửa sổ đến góc dưới bên phải
def move_to_bottom_right(self, position=None):
    screen = self.screen().availableGeometry()
    x = screen.right() - self.width() - (position if position is not None else 10)
    y = screen.bottom() - self.height() - (position if position is not None else 10)
    self.move(QPoint(x, y))

# Thêm hàm back_to_main để đóng cửa sổ và gọi hàm on_back nếu có
def back_to_main(self):
    self.close()
    if callable(self.on_back):
        self.on_back()

def smart_type(text: str):
    if is_feature_enabled("Human type"):
        human_type_handler(text)
    else:
        keyboard.write(text)
