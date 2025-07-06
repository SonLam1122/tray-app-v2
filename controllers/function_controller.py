import logic.funtion_logic as logic
from logic.funtion_logic import BASE32_REGEX
import keyboard
from logic.funtion_logic import execute_action, PartBuffer


class Function1Controller:
    def __init__(self):
        self.actions = [
            "Sinh mã OTP từ 2FA Key",  
            "Dán từng phần chuỗi có dấu |"
        ]

    def get_available_actions(self):
        return self.actions

    def bind_hotkeys(self, get_selected_action, on_data_updated=None):
        def wrapped_execute_otp():
            selected_action = get_selected_action()
            execute_action(selected_action)
            if on_data_updated:
                on_data_updated()

        def wrapped_execute_split():
            selected_action = get_selected_action()
            execute_action(selected_action)
            if on_data_updated:
                on_data_updated()
        
        keyboard.add_hotkey("ctrl+f1", wrapped_execute_otp, suppress=True)
        keyboard.add_hotkey("ctrl+f2", wrapped_execute_split, suppress=True)

        for i in range(9):
            def make_cb(idx):
                def cb():
                    selected_action = get_selected_action()
                    if selected_action is not None and len(PartBuffer) > idx:
                        text = PartBuffer[idx]
                        keyboard.write(text)
                return cb
            keyboard.add_hotkey(f"ctrl+{i+1}", make_cb(i), suppress=True)

    def try_update_2fa_key(self, text):
        if BASE32_REGEX.match(text):
            logic.Current2FAKey = text
            return True
        return False

    def try_update_part_buffer(self, text):
        if '|' in text:
            parts = [p.strip() for p in text.split('|')]
            if 2 <= len(parts) <= 10:
                logic.PartBuffer[:] = parts
                return True
        logic.PartBuffer.clear()
        return False
