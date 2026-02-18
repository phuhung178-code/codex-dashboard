# Dashboard Doanh Số (Streamlit)

Ứng dụng dashboard đơn giản bằng **Python Streamlit** để đọc dữ liệu từ file:

- `DoanhSo_0_160_260201_260215.xlsx`

## Tính năng

- Hiển thị **Tổng doanh số**.
- Hiển thị **Doanh số theo ngày** (nếu file có cột ngày).
- Hiển thị **Doanh số theo ngành hàng**.
- Hiển thị một phần dữ liệu gốc để kiểm tra nhanh.

## Cài đặt

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Chạy ứng dụng

```bash
streamlit run app.py
```

Mặc định app sẽ đọc file Excel tại cùng thư mục dự án:

- `DoanhSo_0_160_260201_260215.xlsx`

## Ghi chú

- App tự dò cột doanh số theo thứ tự ưu tiên: `TT.Bán (VAT) đã giảm trừ`, `TT.Bán`, ...
- App tự dò cột ngành hàng theo các cột phổ biến như `Class`, `Dept.`, ...
- Nếu không có cột ngày, app sẽ hiển thị thông báo hướng dẫn thêm cột ngày để lên biểu đồ theo ngày.
