# Kế hoạch Triển khai - Tái cấu trúc & Thiết kế Dự án Narthang

Kế hoạch này phác thảo các bước để chuyển đổi bộ sưu tập các file HTML hiện tại thành một dự án web có cấu trúc và được thiết kế chuyên nghiệp.

## Mục cần Người dùng Đánh giá

> [!IMPORTANT]
> Tôi sẽ đổi tên một số file để tuân theo các tiêu chuẩn web (chữ thường, không có dấu cách, dùng dấu gạch nối thay cho dấu cách). Điều này sẽ làm hỏng các liên kết hiện có, mà sau đó tôi sẽ sửa lại trong file `index.html` (Trang chủ).

## Các thay đổi Đề xuất

### 1. Cấu trúc Thư mục [MỚI]
Tôi sẽ tổ chức dự án theo cấu trúc sau:
- `/css/`: Chứa các file style
- `/js/`: Chứa các script
- `/assets/img/`: Chứa hình ảnh
- `/pages/`: Chứa các trang con (Phần I, II, III)

### 2. Đổi tên & Tổ chức File [CHỈNH SỬA/DI CHUYỂN]
- `Trang chu.html` → `index.html`
- `Narthang Tumton.html` → `pages/thanh-to-tumton.html`
- [Atisha.html](file:///Users/yogiphil/Desktop/WEB%20DEVELOPMENT%20PROJECT/EXAMPLE1/Atisha.html) → `pages/atisha-dipamkara.html`
- [Shakyamunie.html](file:///Users/yogiphil/Desktop/WEB%20DEVELOPMENT%20PROJECT/EXAMPLE1/Shakyamunie.html) → `pages/shakyamuni.html`
- [Tara.html](file:///Users/yogiphil/Desktop/WEB%20DEVELOPMENT%20PROJECT/EXAMPLE1/Tara.html) → `pages/tara.html`
- [WhiteTara.html](file:///Users/yogiphil/Desktop/WEB%20DEVELOPMENT%20PROJECT/EXAMPLE1/WhiteTara.html) → `pages/white-tara.html`
- `Ạmitayus.html` → `pages/amitayus.html`
- `portal narthang.html` → `pages/portal-narthang.html`

### 3. Hệ thống Style [MỚI]
#### `css/narthang-style.css`
Tôi sẽ tạo một hệ thống thiết kế cao cấp bao gồm:
- **Typography (Phông chữ)**: Sử dụng Google Fonts (ví dụ: 'Cinzel' cho tiêu đề, 'Inter' cho nội dung).
- **Bảng màu**: Đỏ thẫm (#4A0404), Vàng đồng (#D4AF37), Ngọc lam (#40E0D0).
- **Thành phần**: Thanh điều hướng, phần hero (giới thiệu), và các thẻ (cards) sang trọng cho các vị Phật/Đạo sư.

### 4. Logic [MỚI]
#### `js/mantra-engine.js`
Tạo một script mẫu cho "Mantra Engine" như đã yêu cầu trong [Plaintext.html](file:///Users/yogiphil/Desktop/WEB%20DEVELOPMENT%20PROJECT/EXAMPLE1/Plaintext.html).

## Kế hoạch Xác minh

### Kiểm tra Tự động
- Không áp dụng (Dự án thuần HTML/CSS)

### Kiểm tra Thủ công
1. Mở `index.html` trong trình duyệt.
2. Xác minh các liên kết điều hướng đến thư mục `pages/` hoạt động chính xác.
3. Xác minh file `narthang-style.css` được tải và áp dụng cho tất cả các trang.
4. Kiểm tra khả năng tương thất trên web di động bằng công cụ nhà phát triển của trình duyệt.
