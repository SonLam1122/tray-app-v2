import logic.funtion_logic as logic
from logic.funtion_logic import BASE32_REGEX
import keyboard
from logic.funtion_logic import PartBuffer, execute_action 


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
            if selected_action == "Sinh mã OTP từ 2FA Key":
                execute_action(selected_action)
                if on_data_updated:
                    on_data_updated()
                    
        def paste_by_index():
            global CurrentIndex, PartBuffer
            try:
                idx = int(logic.CurrentIndex) - 1
                if 0 <= idx < len(logic.PartBuffer):
                    text_to_paste = logic.PartBuffer[idx]
                    keyboard.write(text_to_paste)
                    logic.CurrentIndex += 1
                    if logic.CurrentIndex > len(logic.PartBuffer):
                        logic.CurrentIndex = 1
            except (ValueError, IndexError) as e:
                print(f"Lỗi khi dán theo chỉ mục: {e}")
                
        def wrapped_paste_by_index():
            paste_by_index()
            if on_data_updated:
                on_data_updated()
    
            
        keyboard.add_hotkey("ctrl+f1", wrapped_execute_otp, suppress=True)
        keyboard.add_hotkey("ctrl+shift+v", wrapped_paste_by_index, suppress=True)

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
                logic.CurrentIndex = 1
                return True
        logic.PartBuffer.clear()
        return False
