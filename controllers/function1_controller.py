import logic.funtion1_logic as logic
from logic.funtion1_logic import BASE32_REGEX
import keyboard
from PyQt5.QtCore import QTimer
import pyperclip
from util.util import smart_type


class Function1Controller:
    def __init__(self):
        self.actions = [
            "Sinh mã OTP từ 2FA Key",  
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
                
        keyboard.add_hotkey("shift+f1", wrapped_execute_otp, suppress=True)
        keyboard.add_hotkey("shift+f1", wrapped_convert_cookie_to_json, suppress=True)

    def try_update_2fa_key(self, text):
        if BASE32_REGEX.match(text):
            logic.Current2FAKey = text
            return True
        return False
