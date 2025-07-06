import pyperclip
import time
import hmac
import base64
import struct
import hashlib
import keyboard
import re

# Biến toàn cục lưu key và buffer
Current2FAKey = None
PartBuffer = []
LastValidClipboard = None

# Regex kiểm tra key 2FA hợp lệ
BASE32_REGEX = re.compile(r'^[A-Z2-7]{16,}$')

# Hàm sinh mã OTP chuẩn TOTP
def generate_totp(secret):
    key = base64.b32decode(secret, casefold=True)
    timestep = int(time.time()) // 30
    msg = struct.pack('>Q', timestep)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = h[19] & 15
    code = (struct.unpack('>I', h[o:o+4])[0] & 0x7fffffff) % 1000000
    return f'{code:06d}'

def execute_action(action):
    global Current2FAKey, PartBuffer, LastValidClipboard
    if action == "Sinh mã OTP từ 2FA Key":
        # Lấy clipboard
        clipboard = pyperclip.paste().strip()
        
        # Nếu clipboard là key hợp lệ, lưu lại
        if BASE32_REGEX.match(clipboard):
            Current2FAKey = clipboard
        if not Current2FAKey:
            return
        
        # Sinh mã OTP
        otp = generate_totp(Current2FAKey)
        
        # Dán mã OTP
        pyperclip.copy(otp)
        keyboard.write(otp)
        print(f"OTP: {otp}")
        
    elif action == "Dán từng phần chuỗi có dấu |":
        clipboard = pyperclip.paste().strip()
        if clipboard != LastValidClipboard and '|' in clipboard:
            parts = [p.strip() for p in clipboard.split('|')]
            if 2 <= len(parts) <= 10:
                PartBuffer[:] = parts
                LastValidClipboard = clipboard
            else:
                PartBuffer.clear()