import random
import string
import sys
import threading
import mouse
import pyperclip
import time
import keyboard
import pygetwindow as gw

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
    try:
        idx = int(CurrentIndex) - 1
        if 0 <= idx < len(PartBuffer):
            text_to_paste = PartBuffer[idx]
            if is_feature_enabled("Human type"):
                human_type_handler(text_to_paste)
            else:
                keyboard.write(text_to_paste)
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

def focus_previous_window():
    try:
        
        # Lấy tiêu đề cửa sổ app của bạn (giả sử là 'TrayApp' hoặc tên file main)
        my_titles = [w.title for w in gw.getAllWindows() if w.isActive]
        # Lấy tất cả cửa sổ ngoài app của bạn
        windows = [w for w in gw.getAllWindows() if w.title and not any(t in w.title for t in my_titles)]
        # Ưu tiên cửa sổ đang mở và có thể activate
        for win in windows:
            try:
                win.activate()
                return True
            except Exception:
                continue
    except Exception as e:
        print(f"[focus_previous_window] Lỗi: {e}")
    return False


def human_type_handler(text: str):
    typing_speed = 0.12
    thinking_chance = 0.03
    thinking_pause_range = (1.0, 2.0)
    error_count = 0

    # Tự động chuyển focus về cửa sổ trước đó
    focus_previous_window()
    time.sleep(0.5)  # Đợi hệ điều hành chuyển focus

    for mod in ['alt', 'ctrl', 'shift', 'windows']:
        try:
            keyboard.release(mod)
        except Exception:
            pass

    # Chờ cho đến khi người dùng thả hết các phím modifier, có timeout
    start = time.time()
    while any(keyboard.is_pressed(mod) for mod in ['alt', 'ctrl', 'shift', 'windows']):
        for mod in ['alt', 'ctrl', 'shift', 'windows']:
            try:
                keyboard.release(mod)
            except Exception:
                pass
        time.sleep(0.05)
        if time.time() - start > 2.0:
            break

    if len(text) < 100 and all(ord(c) < 128 for c in text):
        for char in text:
            try:
                if random.random() < thinking_chance:
                    time.sleep(random.uniform(*thinking_pause_range))
                keyboard.write(char)
                if char in '.!,?':
                    delay = random.uniform(typing_speed * 2.0, typing_speed * 3.0)
                elif char.isspace():
                    delay = random.uniform(typing_speed * 1.5, typing_speed * 2.5)
                else:
                    delay = random.uniform(typing_speed * 0.5, typing_speed * 1.2)
                time.sleep(delay)
            except Exception as e:
                error_count += 1
                if error_count >= 2:
                    pyperclip.copy(text)
                    keyboard.press_and_release('ctrl+v')
                    break
    else:
        pyperclip.copy(text)
        keyboard.press_and_release('ctrl+v')
        time.sleep(0.1)


def force_release_modifiers():
    for mod in ['alt', 'ctrl', 'shift', 'windows']:
        try:
            keyboard.release(mod)
        except Exception:
            pass

