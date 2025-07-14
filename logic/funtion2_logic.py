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
    """Giả lập hành vi gõ phím của người dùng khi in chuỗi văn bản."""
    # Cấu hình các thông số mô phỏng (có thể điều chỉnh):
    typing_speed = 0.1         # Tốc độ gõ cơ bản (giây mỗi ký tự, trung bình)
    error_chance = 0.05        # Xác suất xảy ra lỗi gõ (gõ sai ký tự)
    thinking_chance = 0.05     # Xác suất tạm dừng lâu (giả lập đang suy nghĩ)
    thinking_pause_range = (1.0, 2.0)  # Khoảng thời gian dừng (giây) khi "suy nghĩ"
    punctuation_pause_factor = 3      # Hệ số tăng thời gian dừng sau dấu câu (. , ! ?)
    space_pause_factor = 2           # Hệ số tăng thời gian dừng tại khoảng trắng (giữa các từ)
    max_error_chars = 2              # Số ký tự tối đa sẽ gõ sai trước khi xoá để sửa
    
    for char in text:
        # Tạm dừng lâu như đang suy nghĩ
        if random.random() < thinking_chance:
            time.sleep(random.uniform(*thinking_pause_range))

        # Giả lập lỗi gõ sai
        if random.random() < error_chance:
            wrong_count = random.randint(1, max_error_chars)
            wrong_chars = []
            for _ in range(wrong_count):
                wrong_char = char
                while wrong_char == char:
                    if char.isalpha():
                        pool = [c for c in 'abcdefghijklmnopqrstuvwxyz' if c.lower() != char.lower()]
                        wrong_char = random.choice(pool)
                        if char.isupper():
                            wrong_char = wrong_char.upper()
                    elif char.isdigit():
                        pool = [c for c in '0123456789' if c != char]
                        wrong_char = random.choice(pool)
                    else:
                        pool = 'abcdefghijklmnopqrstuvwxyz'
                        wrong_char = random.choice(pool)
                wrong_chars.append(wrong_char)
                keyboard.write(wrong_char)
                time.sleep(random.uniform(typing_speed * 0.5, typing_speed * 1.5))
            
            for _ in range(len(wrong_chars)):
                keyboard.send('backspace')
                time.sleep(random.uniform(typing_speed * 0.5, typing_speed * 1.0))

        keyboard.write(char)

        if char in '.!,?':
            delay = random.uniform(typing_speed * punctuation_pause_factor * 0.5,
                                    typing_speed * punctuation_pause_factor * 1.5)
        elif char.isspace():
            delay = random.uniform(typing_speed * space_pause_factor * 0.5,
                                    typing_speed * space_pause_factor * 1.5)
        else:
            delay = random.uniform(typing_speed * 0.5, typing_speed * 1.5)
        time.sleep(delay)
