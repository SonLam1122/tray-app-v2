# TrayApp - Công cụ OTP & Cắt chuỗi nhanh từ khay hệ thống

## Giới thiệu

**TrayApp** là một ứng dụng nhỏ gọn chạy nền dưới **System Tray**, hỗ trợ bạn thao tác cực nhanh với:

- **Sinh mã OTP (TOTP)** từ mã 2FA (secret key)
- **Cắt chuỗi có dấu `|`** và lấy nhanh từng phần bằng phím tắt

Chỉ cần **copy chuỗi vào clipboard**, bấm **hotkey**, và phần cần dùng sẽ tự động được copy trở lại clipboard – sẵn sàng để dán ở bất kỳ đâu.

---

## Chức năng chính

### Lấy mã OTP từ secret key 2FA

- **Cách sử dụng**:
  1. Copy chuỗi secret key (ví dụ: `JBSWY3DPEHPK3PXP`) vào clipboard
  2. Nhấn tổ hợp **`Ctrl + F1`**
  3. Mã OTP 6 chữ số sẽ được sinh tự động và copy lại vào clipboard

- ✅ Không cần cấu hình
- ✅ Mã OTP được xử lý cục bộ, đảm bảo bảo mật

---

### Cắt chuỗi theo dấu `|` và lấy từng phần

- **Cách sử dụng**:
  1. Copy chuỗi dạng sau vào clipboard:
     ```
     username|password|email@example.com|0123456789
     ```
  2. Nhấn tổ hợp phím:
     - `Ctrl + 1` → Copy `username` vào clipboard
     - `Ctrl + 2` → Copy `password`
     - `Ctrl + 3` → Copy `email@example.com`
     - ...
     - `Ctrl + 9` → Copy phần tử thứ 9 (nếu có)

- ✅ Dễ dàng thao tác bằng phím
- ✅ Không cần cửa sổ giao diện, chỉ cần clipboard

---

## Hotkey mặc định

| Phím tắt           | Tác vụ                             |
|--------------------|-------------------------------------|
| `Ctrl + F1`         | Lấy mã OTP từ secret key 2FA        |
| `Ctrl + 1` → `Ctrl + 9` | Lấy phần thứ 1 → 9 từ chuỗi `|`     |

---

## Ví dụ thực tế

**Chuỗi đã copy:**
admin|123456|admin@example.com|0987654321
| Hotkey     | Kết quả (vào clipboard)     |
|------------|-----------------------------|
| `Ctrl + 1` | `admin`                     |
| `Ctrl + 2` | `123456`                    |
| `Ctrl + 3` | `admin@example.com`         |
| `Ctrl + 4` | `0987654321`                |

Sau khi nhấn hotkey, chỉ cần `Ctrl + V` để dán ra nội dung đã lấy.

---

## Bảo mật

- OTP được tạo hoàn toàn cục bộ
- Không lưu trữ bất kỳ thông tin nào của người dùng
- Clipboard sẽ được ghi đè khi dùng hotkey để tránh lộ thông tin trước đó

---
