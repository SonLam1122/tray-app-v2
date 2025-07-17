import logic.funtion1_logic as logic
from logic.funtion1_logic import BASE32_REGEX
import keyboard
from logic.funtion1_logic import PartBuffer
from PyQt5.QtCore import QTimer
import pyperclip
from util.util import smart_type


class Function1Controller:
    def __init__(self):
        self.actions = [
            "Sinh mã OTP từ 2FA Key",  
            "Dán từng phần chuỗi có dấu |",
            "Convert Cookie sang JSON",
        ]

    def get_available_actions(self):
        return self.actions

    def bind_hotkeys(self, get_selected_action, on_data_updated=None):
        def wrapped_execute_otp():
            selected_action = get_selected_action()
            if selected_action == "Sinh mã OTP từ 2FA Key":
                otp = logic.otp()
                pyperclip.copy(otp)
                smart_type(otp)
                print(f"OTP: {otp}")
                if on_data_updated:
                    on_data_updated()
        
        def wrapped_paste_by_index():
            if get_selected_action() == "Dán từng phần chuỗi có dấu |":
                paste_by_index()
                if on_data_updated:
                    on_data_updated()

        def wrapped_convert_cookie_to_json():
            if get_selected_action() == "Convert Cookie sang JSON":
                try:
                    if logic.CurrentCookieJson:
                        json = logic.CurrentCookieJson
                        smart_type(json)
                except Exception as e:
                    print(f"[!] Cookie convert error: {e}")

                if on_data_updated:
                    QTimer.singleShot(0, on_data_updated)
                
        def paste_by_index():
            global CurrentIndex, PartBuffer
            try:
                idx = int(logic.CurrentIndex) - 1
                if 0 <= idx < len(logic.PartBuffer):
                    text_to_paste = logic.PartBuffer[idx]
                    smart_type(text_to_paste)
                    logic.CurrentIndex += 1
                    if logic.CurrentIndex > len(logic.PartBuffer):
                        logic.CurrentIndex = 1
            except (ValueError, IndexError) as e:
                print(f"Lỗi khi dán theo chỉ mục: {e}")
                
        keyboard.add_hotkey("ctrl+f1", wrapped_execute_otp, suppress=True)
        keyboard.add_hotkey("ctrl+shift+v", wrapped_paste_by_index, suppress=True)
        keyboard.add_hotkey("ctrl+f2", wrapped_convert_cookie_to_json, suppress=True)

    def try_update_2fa_key(self, text):
        if BASE32_REGEX.match(text):
            logic.Current2FAKey = text
            return True
        return False

    def try_update_part_buffer(self, text):
        if '|' in text:
            parts = [p.strip() for p in text.split('|')]
            logic.PartBuffer[:] = parts
            logic.CurrentIndex = 1
            return True
        logic.PartBuffer.clear()
        return False
