# TrayApp - Công cụ OTP & Dán chuỗi tuần tự

## 🏙️ Giới thiệu

**TrayApp** là một ứng dụng cửa sổ nhỏ gọn, luôn nổi trên các ứng dụng khác, giúp bạn tăng tốc công việc hàng ngày với hai tính năng chính:

* **Sinh mã OTP (TOTP)** tức thì từ mã 2FA (secret key).
* **Dán tuần tự từng phần** của một chuỗi được ngăn cách bởi dấu `|`.

Ứng dụng được thiết kế để tối ưu hóa quy trình làm việc: chỉ cần **sao chép (copy)** dữ liệu vào clipboard, chọn chức năng, và dùng **phím tắt (hotkey)**. Mọi thứ diễn ra nhanh chóng và tiện lợi ngay tại góc màn hình của bạn.

---

## ✨ Chức năng chính

### 1. Sinh mã OTP từ secret key 2FA

Chức năng này giúp bạn lấy mã xác thực hai yếu tố mà không cần mở điện thoại.

* **Cách sử dụng**:
    1.  Trên cửa sổ ứng dụng, chọn chức năng **"Sinh mã OTP từ 2FA Key"**.
    2.  Sao chép (Copy) chuỗi secret key của bạn (ví dụ: `JBSWY3DPEHPK3PXP`) vào clipboard.
    3.  Nhấn tổ hợp phím **`Ctrl + F1`**.
    4.  Mã OTP gồm 6 chữ số sẽ ngay lập tức được dán vào vị trí con trỏ của bạn.

* ✅ **An toàn**: Mã được tạo hoàn toàn trên máy tính của bạn và không gửi đi bất kỳ đâu.
* ✅ **Tiện lợi**: Không cần cấu hình phức tạp, chỉ cần sao chép và bấm phím tắt.

### 2. Dán tuần tự từng phần của chuỗi

Tính năng độc đáo này cho phép bạn dán lần lượt từng phần của một chuỗi văn bản (ví dụ: thông tin đăng nhập, địa chỉ) một cách dễ dàng.

* **Cách sử dụng**:
    1.  Trên cửa sổ ứng dụng, chọn chức năng **"Dán từng phần chuỗi có dấu |"**.
    2.  Sao chép một chuỗi có các phần được ngăn cách bởi dấu `|` vào clipboard.
        ```
        username|password|email@example.com|0123456789
        ```
    3.  Ứng dụng sẽ tự động nhận diện và chia chuỗi thành các phần trong bộ đệm.
    4.  Nhấn phím tắt **`Ctrl + Shift + V`** để dán phần tử đầu tiên (`username`).
    5.  Nhấn **`Ctrl + Shift + V`** một lần nữa để dán phần tử tiếp theo (`password`), và cứ tiếp tục như vậy.
    6.  Khi dán hết các phần, chỉ mục sẽ tự động quay về phần tử đầu tiên.

* ✅ **Hiệu quả**: Tăng tốc độ nhập liệu lặp đi lặp lại chỉ với một phím tắt duy nhất.
* ✅ **Linh hoạt**: Bạn có thể xem và chỉnh sửa trực tiếp các phần đã cắt ngay trên giao diện ứng dụng.

---

## 🖥️ Giao diện ứng dụng

TrayApp cung cấp một cửa sổ điều khiển nhỏ gọn, luôn hiển thị ở góc dưới cùng bên phải màn hình.

* **Chọn chức năng**: Dùng nút `RadioButton` để chuyển đổi giữa hai tính năng.
* **Khu vực chức năng "Dán từng phần"**:
    * **Index**: Hiển thị và cho phép bạn thay đổi vị trí của phần tử sắp được dán.
    * **Bộ đệm (Buffer)**: Một ô văn bản hiển thị tất cả các phần đã được cắt ra. Bạn có thể chỉnh sửa, thêm hoặc xóa các phần trực tiếp tại đây.
* **Hiển thị trạng thái**:
    * `🔑`: Hiển thị mã 2FA Key hợp lệ cuối cùng mà ứng dụng nhận được từ clipboard.
* **Nút ❌**: Nhấn để thoát ứng dụng.

---

## ⌨️ Hotkey mặc định

| Phím tắt | Tác vụ |
| :--- | :--- |
| `Ctrl + F1` | Sinh và dán mã OTP từ secret key đã sao chép. |
| `Ctrl + Shift + V` | Dán phần tử hiện tại từ chuỗi và tự động chuyển con trỏ đến phần tử tiếp theo. |

---

## 🚀 Cài đặt và Chạy ứng dụng

**Yêu cầu:** Python 3

1.  **Cài đặt các thư viện cần thiết:**
    Mở terminal (hoặc Command Prompt) và chạy lệnh:
    ```bash
    pip install PyQt5 pyperclip keyboard
    ```

2.  **Chạy ứng dụng:**
    Di chuyển đến thư mục chứa mã nguồn và thực thi tệp `main.py`:
    ```bash
    python main.py
    ```

---

## 🔒 Bảo mật

* Mã OTP được tạo hoàn toàn cục bộ trên máy tính của bạn bằng thuật toán TOTP tiêu chuẩn.
* Ứng dụng không lưu trữ bất kỳ thông tin nhạy cảm nào của bạn.
* Dữ liệu trong clipboard được xử lý và ghi đè ngay lập tức để bảo vệ thông tin.
