import logic.funtion1_logic as logic
from logic.funtion1_logic import BASE32_REGEX
import keyboard
from PyQt5.QtCore import QTimer
import pyperclip
from logic.funtion2_logic import is_feature_enabled, human_type_handler
import threading
import ctypes
import ctypes.wintypes
import atexit


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
            for mod in ['alt', 'ctrl', 'shift', 'windows']:
                try:
                    keyboard.release(mod)
                except Exception:
                    pass
            selected_action = get_selected_action()
            if selected_action == "Sinh mã OTP từ 2FA Key":
                otp = logic.otp()
                pyperclip.copy(otp)
                if is_feature_enabled("Human type"):
                    human_type_handler(otp)
                else:
                    keyboard.write(otp)
                print(f"OTP: {otp}")
                if on_data_updated:
                    on_data_updated()
        
        def wrapped_convert_cookie_to_json():
            for mod in ['alt', 'ctrl', 'shift', 'windows']:
                try:
                    keyboard.release(mod)
                except Exception:
                    pass
            if get_selected_action() == "Convert Cookie sang JSON":
                try:
                    if logic.CurrentCookieJson:
                        json = logic.CurrentCookieJson
                        pyperclip.copy(json)
                        if is_feature_enabled("Human type"):
                            human_type_handler(json)
                        else:
                            keyboard.write(json)
                except Exception as e:
                    print(f"[!] Cookie convert error: {e}")

                if on_data_updated:
                    QTimer.singleShot(0, on_data_updated)
                
        # --- Hook phím toàn cục bằng ctypes ---
        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32
        WH_KEYBOARD_LL = 13
        WM_KEYDOWN = 0x0100
        WM_KEYUP = 0x0101
        VK_Q = 0x51
        VK_W = 0x57
        VK_CONTROL = 0x11
        pressed_ctrl = [False]

        class KBDLLHOOKSTRUCT(ctypes.Structure):
            _fields_ = [
                ("vkCode", ctypes.wintypes.DWORD),
                ("scanCode", ctypes.wintypes.DWORD),
                ("flags", ctypes.wintypes.DWORD),
                ("time", ctypes.wintypes.DWORD),
                ("dwExtraInfo", ctypes.POINTER(ctypes.wintypes.ULONG))
            ]

        def low_level_keyboard_proc(nCode, wParam, lParam):
            if nCode == 0:
                kb = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
                if wParam == WM_KEYDOWN:
                    if kb.vkCode == VK_CONTROL:
                        pressed_ctrl[0] = True
                    elif kb.vkCode == VK_Q and pressed_ctrl[0]:
                        wrapped_execute_otp()
                        return 1  # Chặn phím này
                    elif kb.vkCode == VK_W and pressed_ctrl[0]:
                        wrapped_convert_cookie_to_json()
                        return 1
                elif wParam == WM_KEYUP:
                    if kb.vkCode == VK_CONTROL:
                        pressed_ctrl[0] = False
            return user32.CallNextHookEx(None, nCode, wParam, lParam)

        CMPFUNC = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p)
        pointer = CMPFUNC(low_level_keyboard_proc)
        hook_id = [None]

        def start_hook():
            hook_id[0] = user32.SetWindowsHookExA(WH_KEYBOARD_LL, pointer, kernel32.GetModuleHandleW(None), 0)
            import pythoncom
            pythoncom.PumpMessages()

        def unhook():
            if hook_id[0]:
                user32.UnhookWindowsHookEx(hook_id[0])
        atexit.register(unhook)

        threading.Thread(target=start_hook, daemon=True).start()
        # --- End hook ---

        keyboard.add_hotkey("ctrl+q", wrapped_execute_otp, suppress=True)
        keyboard.add_hotkey("ctrl+w", wrapped_convert_cookie_to_json, suppress=True)

    def try_update_2fa_key(self, text):
        if BASE32_REGEX.match(text):
            logic.Current2FAKey = text
            return True
        return False
