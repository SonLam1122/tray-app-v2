# TrayApp v2 - Trợ lý Tăng tốc Công việc Của Bạn

## 🏙️ Giới thiệu

**TrayApp v2** là một ứng dụng tiện ích nhỏ gọn, được thiết kế để luôn nổi trên các cửa sổ khác, giúp bạn tự động hóa và tăng tốc các tác vụ lặp đi lặp lại hàng ngày. Với giao diện trực quan và các phím tắt mạnh mẽ, TrayApp v2 là người bạn đồng hành không thể thiếu để tối ưu hóa quy trình làm việc của bạn.

Ứng dụng được xây dựng dựa trên triết lý "sao chép và thực thi": bạn chỉ cần sao chép dữ liệu cần xử lý vào clipboard, chọn chức năng, và nhấn phím tắt. Mọi thứ diễn ra ngay lập tức, giúp bạn tiết kiệm thời gian và công sức.

---

## ✨ Các Chức Năng Chính

TrayApp v2 được chia thành hai nhóm chức năng chính: **Function 1 (Chức năng Radio)** và **Function 2 (Chức năng Bật/Tắt)**.

### Function 1: Các Tác Vụ Đơn Lẻ

Đây là nhóm các chức năng hoạt động độc lập, được chọn thông qua các nút radio trên giao diện.

#### 1. Sinh mã OTP từ 2FA Key

* **Mô tả:** Tự động tạo và dán mã xác thực hai yếu tố (2FA) mà không cần dùng đến điện thoại.
* **Cách sử dụng:**
    1.  Chọn chức năng **"Sinh mã OTP từ 2FA Key"**.
    2.  Sao chép (Copy) chuỗi Secret Key 2FA của bạn (ví dụ: `JBSWY3DPEHPK3PXP`). Ứng dụng sẽ tự động nhận diện và lưu lại key này.
    3.  Đặt con trỏ vào ô bạn muốn nhập mã.
    4.  Nhấn tổ hợp phím **`Ctrl + F1`**. Mã OTP gồm 6 chữ số sẽ ngay lập tức được dán vào.
* **An toàn:** Mã OTP được tạo hoàn toàn trên máy tính của bạn bằng thuật toán TOTP tiêu chuẩn và không được gửi đi bất cứ đâu.

#### 2. Dán Tuần Tự Từng Phần Của Chuỗi

* **Mô tả:** Một tính năng độc đáo giúp bạn dán lần lượt từng phần của một chuỗi văn bản được phân cách bởi dấu `|`. Rất hữu ích khi cần điền các biểu mẫu đăng nhập, thông tin cá nhân, v.v.
* **Cách sử dụng:**
    1.  Chọn chức năng **"Dán từng phần chuỗi có dấu |"**.
    2.  Sao chép một chuỗi có các phần được ngăn cách bởi dấu `|`. Ví dụ: `tendangnhap|matkhau123|email@example.com`.
    3.  Ứng dụng sẽ tự động chia chuỗi thành các phần và hiển thị trong bộ đệm (buffer) trên giao diện.
    4.  Nhấn phím tắt **`Ctrl + Shift + V`** để dán phần tử đầu tiên (`tendangnhap`).
    5.  Nhấn tiếp **`Ctrl + Shift + V`** để dán phần tử tiếp theo (`matkhau123`), và cứ thế tiếp tục.
    6.  Khi đã dán hết các phần, chỉ mục sẽ tự động quay về phần tử đầu tiên.
* **Linh hoạt:** Bạn có thể xem, chỉnh sửa, thêm hoặc xóa các phần tử trực tiếp trong ô bộ đệm trên giao diện ứng dụng.

#### 3. Chuyển Đổi Cookie sang JSON

* **Mô tả:** Nhanh chóng chuyển đổi một chuỗi cookie chuẩn (được phân cách bởi dấu `;`) thành định dạng JSON đẹp mắt và dễ đọc.
* **Cách sử dụng:**
    1.  Chọn chức năng **"Convert Cookie sang JSON"**.
    2.  Sao chép chuỗi cookie vào clipboard.
    3.  Nhấn phím tắt **`Ctrl + F2`**. Chuỗi JSON tương ứng sẽ được dán vào vị trí con trỏ của bạn.
    4.  Bạn cũng có thể xem trước kết quả JSON ngay trên giao diện ứng dụng.

---

### Function 2: Các Tiện Ích Nền

Đây là nhóm các tính năng có thể được bật hoặc tắt để chạy nền và hỗ trợ bạn trong quá trình làm việc.

#### 1. Double Click để Sao Chép

* **Mô tả:** Loại bỏ nhu cầu phải nhấn `Ctrl + C`. Chỉ cần bôi đen văn bản bằng cách double-click (hoặc kéo chuột), ứng dụng sẽ tự động sao chép nội dung đó vào clipboard.
* **Cách kích hoạt:**
    1.  Vào mục **"Function 2 (On/Off)"**.
    2.  Bật công tắc bên cạnh tính năng **"Double click để sao chép"**.

#### 2. Gõ Phím Kiểu Người (Human Typing)

* **Mô tả:** Khi được bật, tất cả các tác vụ dán văn bản của TrayApp v2 (OTP, dán tuần tự, cookie) sẽ được thực hiện bằng cách mô phỏng hành vi gõ phím của con người, bao gồm cả việc dừng nghỉ, gõ sai và sửa lại. Điều này cực kỳ hữu ích để vượt qua các cơ chế chống bot trên một số trang web.
* **Cách kích hoạt:**
    1.  Vào mục **"Function 2 (On/Off)"**.
    2.  Bật công tắc bên cạnh tính năng **"Human type"**.

---

## ⌨️ Bảng Phím Tắt (Hotkey)

| Phím tắt | Tác vụ | Chức năng yêu cầu |
| :--- | :--- | :--- |
| `Ctrl + F1` | Sinh và dán mã OTP. | "Sinh mã OTP từ 2FA Key" |
| `Ctrl + Shift + V` | Dán phần tử tiếp theo trong chuỗi. | "Dán từng phần chuỗi có dấu \|" |
| `Ctrl + F2` | Chuyển đổi và dán Cookie sang JSON. | "Convert Cookie sang JSON" |

---

## 🚀 Cài đặt và Chạy Ứng Dụng

**Yêu cầu:** Python 3

1.  **Cài đặt các thư viện cần thiết:**
    Mở terminal (hoặc Command Prompt) và chạy lệnh sau:
    ```bash
    pip install PyQt5 pyperclip keyboard mouse
    ```

2.  **Chạy ứng dụng:**
    Di chuyển đến thư mục gốc của dự án và thực thi tệp `main.py`:
    ```bash
    python main.py
    ```

---

## 🔒 Bảo Mật

* **Tôn trọng quyền riêng tư của bạn là ưu tiên hàng đầu.**
* Mã OTP được tạo hoàn toàn cục bộ trên máy tính của bạn.
* Ứng dụng **không lưu trữ** bất kỳ thông tin nhạy cảm nào như Secret Key, mật khẩu hay cookie.
* Dữ liệu trong clipboard chỉ được xử lý tạm thời trong bộ nhớ và không được ghi ra bất kỳ đâu.