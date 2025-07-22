from logic.funtion2_logic import start_double_click_copy_monitor, human_type_handler, set_paste_by_index_hotkey
from PyQt5.QtCore import QTimer
import pyperclip

class Function2Controller:
    def __init__(self):
        self.actions = [
            "Double click để sao chép",
            "Human type",
            "Dán từng phần chuỗi có dấu |"
        ]

    def get_available_features(self):
        return self.actions

    def bind_feature(self, selected_feature: str, widget):
        if selected_feature == "Double click để sao chép":
            start_double_click_copy_monitor()
        elif selected_feature == "Dán từng phần chuỗi có dấu |":
            set_paste_by_index_hotkey(True)

    def unbind_feature(self, selected_feature: str):
        if selected_feature == "Dán từng phần chuỗi có dấu |":
            set_paste_by_index_hotkey(False)
