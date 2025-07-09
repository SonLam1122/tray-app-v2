
# TrayApp - Công cụ OTP & Cắt chuỗi nhanh từ khay hệ thống

## Giới thiệu

**TrayApp** là một ứng dụng nhỏ gọn chạy nền, giúp bạn thao tác cực nhanh với:

  - **Sinh mã OTP (TOTP)** từ mã 2FA (secret key)
  - **Cắt chuỗi có dấu `|`** và lấy nhanh từng phần bằng phím tắt

Chỉ cần **sao chép (copy) chuỗi vào clipboard**, chọn chức năng từ cửa sổ ứng dụng, và sử dụng **phím tắt (hotkey)**. Nội dung bạn cần sẽ tự động được sao chép trở lại clipboard, sẵn sàng để dán ở bất kỳ đâu.

-----

## Chức năng chính

### 1\. Lấy mã OTP từ secret key 2FA

  - **Cách sử dụng**:

    1.  Chọn chức năng "Sinh mã OTP từ 2FA Key" trên cửa sổ ứng dụng.
    2.  Sao chép chuỗi secret key (ví dụ: `JBSWY3DPEHPK3PXP`) vào clipboard.
    3.  Nhấn tổ hợp phím **`Ctrl + F1`**.
    4.  Mã OTP gồm 6 chữ số sẽ được sinh tự động và sao chép lại vào clipboard.

  - ✅ Không cần cấu hình phức tạp.

  - ✅ Mã OTP được xử lý hoàn toàn trên máy của bạn, đảm bảo an toàn và bảo mật.

### 2\. Cắt chuỗi theo dấu `|` và lấy từng phần

  - **Cách sử dụng**:

    1.  Chọn chức năng "Dán từng phần chuỗi có dấu |" trên cửa sổ ứng dụng.
    2.  Sao chép một chuỗi theo định dạng sau vào clipboard:
        ```
        username|password|email@example.com|0123456789
        ```
    3.  Cửa sổ ứng dụng sẽ hiển thị các phần đã được cắt.
    4.  Nhấn tổ hợp phím tương ứng để lấy phần bạn muốn:
          - `Ctrl + 1` → Sao chép `username` vào clipboard
          - `Ctrl + 2` → Sao chép `password`
          - `Ctrl + 3` → Sao chép `email@example.com`
          - ...
          - `Ctrl + 9` → Sao chép phần tử thứ 9 (nếu có).

  - ✅ Dễ dàng thao tác chỉ bằng phím tắt.

  - ✅ Hoạt động trực tiếp với clipboard mà không cần giao diện phức tạp.

-----

## Giao diện ứng dụng

Khi chạy, TrayApp sẽ hiển thị một cửa sổ nhỏ gọn, luôn nổi trên các ứng dụng khác ở góc dưới cùng bên phải màn hình.

  - **Chọn chức năng**: Tích vào `RadioButton` để chọn tác vụ bạn muốn thực hiện.
  - **Hiển thị trạng thái**:
      - `🔑`: Hiển thị mã 2FA Key đã được nhận.
      - `📋`: Hiển thị các phần của chuỗi đã được cắt từ clipboard.
  - **Nút ❌**: Nhấn để thoát ứng dụng.

-----

## Hotkey mặc định

| Phím tắt | Tác vụ |
| :--- | :--- |
| `Ctrl + F1` | Lấy mã OTP từ secret key 2FA đã sao chép. |
| `Ctrl + 1` → `Ctrl + 9` | Lấy phần tử thứ 1 đến 9 từ chuỗi đã được cắt. |

-----

## Cài đặt và Chạy ứng dụng

**Yêu cầu:** Cần cài đặt Python 3.

1.  **Cài đặt các thư viện cần thiết:**
    Mở terminal hoặc command prompt và chạy lệnh sau:

    ```bash
    pip install PyQt5 pyperclip keyboard
    ```

2.  **Chạy ứng dụng:**
    Di chuyển đến thư mục chứa mã nguồn và thực thi file `main.py`:

    ```bash
    python main.py
    ```

-----

## Bảo mật

  - Mã OTP được tạo hoàn toàn cục bộ trên máy tính của người dùng.
  - Ứng dụng không lưu trữ bất kỳ thông tin nào của bạn.
  - Clipboard sẽ được ghi đè ngay sau khi sử dụng phím tắt để bảo vệ thông tin.
