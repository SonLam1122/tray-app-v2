import random
import sys
import threading
import mouse
import pyperclip
import time
import keyboard

_click_times = []
_enabled_features = set()
_stop_flags = {}

# Biến toàn cục cho tính năng dán từng phần chuỗi có dấu |
PartBuffer = []
CurrentIndex = 1
LastValidClipboard = None

# Hàm cập nhật buffer khi có chuỗi chứa |
def try_update_part_buffer(text):
    global PartBuffer, CurrentIndex, LastValidClipboard
    if '|' in text:
        parts = [p.strip() for p in text.split('|')]
        PartBuffer[:] = parts
        CurrentIndex = 1
        LastValidClipboard = text
        return True
    PartBuffer.clear()
    return False

def paste_by_index():
    global CurrentIndex, PartBuffer
    import logic.funtion2_logic as logic
    try:
        idx = int(CurrentIndex) - 1
        if 0 <= idx < len(PartBuffer):
            text_to_paste = PartBuffer[idx]
            import util.util as util
            util.smart_type(text_to_paste)
            CurrentIndex += 1
            if CurrentIndex > len(PartBuffer):
                CurrentIndex = 1
    except (ValueError, IndexError) as e:
        print(f"Lỗi khi dán theo chỉ mục: {e}")

# Hàm bật/tắt hotkey cho tính năng này
def set_paste_by_index_hotkey(enabled):
    if enabled:
        keyboard.add_hotkey("ctrl+shift+v", paste_by_index, suppress=True)
    else:
        try:
            keyboard.remove_hotkey("ctrl+shift+v")
        except Exception:
            pass

def is_feature_enabled(name):
    return name in _enabled_features

def set_feature_enabled(name, enabled):
    if enabled:
        _enabled_features.add(name)
        _stop_flags[name] = False
    else:
        _enabled_features.discard(name)
        _stop_flags[name] = True

def get_selected_text():
    keyboard.press_and_release('ctrl+c')
    time.sleep(0.05)
    return pyperclip.paste()

def start_double_click_copy_monitor():
    def on_click():
        now = time.monotonic()
        _click_times.append(now)

        if len(_click_times) > 2:
            _click_times.pop(0)

        if len(_click_times) == 2:
            delta = _click_times[1] - _click_times[0]
            if 0.05 <= delta <= 0.5:
                time.sleep(0.1)  # đợi hệ thống bôi đen
                text = get_selected_text()
                if text.strip():
                    pyperclip.copy(text)
                    print(f"[✔] Copied: {text.strip()}")
                else:
                    print("[⚠️] Không có nội dung để copy.")
                _click_times.clear()

    def monitor():
        mouse.on_click(on_click)
        while not _stop_flags.get("Double click để sao chép", False):
            time.sleep(0.01)
        mouse.unhook_all()

    threading.Thread(target=monitor, daemon=True).start()

def human_type_handler(text: str):
    typing_speed = 0.07
    thinking_chance = 0.03
    thinking_pause_range = (1.0, 2.0)

    for char in text:
        # Thỉnh thoảng dừng lại như đang suy nghĩ
        if random.random() < thinking_chance:
            time.sleep(random.uniform(*thinking_pause_range))

        # Gõ ký tự chính xác
        keyboard.write(char)

        # Nghỉ tùy loại ký tự
        if char in '.!,?':
            delay = random.uniform(typing_speed * 2.0, typing_speed * 3.0)
        elif char.isspace():
            delay = random.uniform(typing_speed * 1.5, typing_speed * 2.5)
        else:
            delay = random.uniform(typing_speed * 0.5, typing_speed * 1.2)

        time.sleep(delay)

