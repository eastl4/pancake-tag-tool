# Công cụ Gắn Tag Pancake

Công cụ Gắn Tag Pancake là một script Python được thiết kế để tự động hoá quá trình gắn tag cho các hội thoại trên nền tảng Pancake.vn. Công cụ này giúp bạn quản lý hội thoại hiệu quả hơn bằng cách áp dụng các tag đã được cấu hình sẵn.

## Tính năng
- Lấy danh sách trang và hội thoại từ Pancake.vn thông qua API.
- Cho phép người dùng chọn trang và tag tương tác.
- Tự động gắn tag vào các hội thoại chưa đọc.
- Chạy ở chế độ live để liên tục kiểm tra hội thoại mới.

## Yêu cầu
- Python 3.6 trở lên được cài đặt trên hệ thống của bạn.
- Một tài khoản Pancake.vn đang hoạt động với quyền truy cập API.

## Cài đặt

1. Clone repository này:
   ```bash
   git clone https://github.com/your-username/pancake-tag-tool.git
   cd pancake-tag-tool
   ```

2. Tạo môi trường ảo (không bắt buộc nhưng được khuyến khích):
   ```bash
   python -m venv venv
   venv\Scripts\activate                     #Trên OS: source venv/bin/activate
   ```

3. Cài đặt các thư viện cần thiết:
   ```bash
   pip install -r requirements.txt
   ```

## Sử dụng

1. Chạy script:
   ```bash
   python src/main.py
   ```

2. Nhập access token API Pancake.vn của bạn khi được yêu cầu.

3. Lựa chọn các trang và tag tương tác theo hướng dẫn từ chương trình.

4. Công cụ sẽ liên tục theo dõi hội thoại và gắn tag vào các hội thoại chưa đọc.

## Cấu hình

Tag được định nghĩa sẵn trong script và có thể tuỳ chỉnh trong biến `TAGS` trong file `src/main.py`. Mỗi tag có các thuộc tính sau:
- `tag_id`
- `color`
- `lighten_color`
- `text`

Ví dụ:
```python
TAGS = [
    {"tag_id": 0, "color": "#4b5577", "lighten_color": "#c9ccd6", "text": "Kiểm hàng"},
    {"tag_id": 1, "color": "#822ba1", "lighten_color": "#d9bfe2", "text": "Câu hỏi"}
]
```

## Lưu ý
- Đảm bảo rằng access token API của bạn có đầy đủ quyền để lấy danh sách trang, hội thoại và gắn tag.
- Script sử dụng khoảng thời gian kiểm tra (polling interval) được định nghĩa trong `POLL_INTERVAL`. Bạn có thể điều chỉnh giá trị này theo giây (mặc định là 5 giây).

