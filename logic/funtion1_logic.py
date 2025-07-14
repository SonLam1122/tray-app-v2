import pyperclip
import time
import hmac
import base64
import struct
import hashlib
import re
import json

# Biến toàn cục lưu key và buffer
Current2FAKey = None
PartBuffer = []
LastValidClipboard = None
CurrentIndex = 1
CurrentCookieJson = ""
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

def otp():
    global Current2FAKey, PartBuffer, LastValidClipboard
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
    return otp
                
def convert_cookie_to_json(text: str) -> str:
    """
    Chuyển chuỗi cookies dạng 'key=value; key2=value2' sang JSON.
    """
    cookie_dict = {}
    parts = text.strip().split(';')
    for part in parts:
        if '=' in part:
            key, value = part.split('=', 1)
            cookie_dict[key.strip()] = value.strip()
    return json.dumps(cookie_dict, indent=2, ensure_ascii=False)