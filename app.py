from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Dashboard Doanh Số", page_icon="📊", layout="wide")

DATA_FILE = "DoanhSo_0_160_260201_260215.xlsx"
DATE_CANDIDATES = [
    "Ngày",
    "Ngay",
    "Date",
    "Transaction Date",
    "Ngày bán",
    "Ngày giao dịch",
]
SALES_CANDIDATES = [
    "TT.Bán (VAT) đã giảm trừ",
    "TT.Bán",
    "Doanh số",
    "Doanh Thu",
    "Sales",
]
CATEGORY_CANDIDATES = [
    "Ngành hàng",
    "Class",
    "Sub Class",
    "Dept.",
    "Sub Dept.",
    "Mã 5NH",
]


def pick_column(df: pd.DataFrame, candidates: list[str]) -> str | None:
    """Chọn cột đầu tiên khớp với danh sách ứng viên."""
    for name in candidates:
        if name in df.columns:
            return name
    return None


@st.cache_data(show_spinner=False)
def load_data(file_path: str) -> pd.DataFrame:
    return pd.read_excel(file_path)


st.title("📊 Dashboard Doanh Số")
st.caption("Ứng dụng Streamlit đọc dữ liệu từ file Excel và trực quan hoá doanh số.")

file_path = Path(DATA_FILE)
if not file_path.exists():
    st.error(f"Không tìm thấy file dữ liệu: {DATA_FILE}")
    st.stop()

try:
    df = load_data(DATA_FILE)
except Exception as exc:  # pragma: no cover - hiển thị lỗi runtime cho người dùng
    st.exception(exc)
    st.stop()

st.subheader("1) Dữ liệu gốc")
st.dataframe(df.head(20), use_container_width=True)

sales_col = pick_column(df, SALES_CANDIDATES)
if sales_col is None:
    st.error(
        "Không tìm thấy cột doanh số. "
        f"Các cột hiện có: {', '.join(map(str, df.columns.tolist()))}"
    )
    st.stop()

# Chuẩn hoá doanh số
work_df = df.copy()
work_df[sales_col] = pd.to_numeric(work_df[sales_col], errors="coerce").fillna(0)

total_sales = work_df[sales_col].sum()

st.subheader("2) Tổng quan")
col1, col2 = st.columns(2)
col1.metric("Tổng doanh số", f"{total_sales:,.0f}")
col2.metric("Số dòng dữ liệu", f"{len(work_df):,}")

st.subheader("3) Doanh số theo ngày")
date_col = pick_column(work_df, DATE_CANDIDATES)
if date_col is None:
    st.info(
        "Không tìm thấy cột ngày trong file nên chưa thể vẽ biểu đồ doanh số theo ngày. "
        "Bạn có thể thêm một cột như 'Ngày' hoặc 'Transaction Date'."
    )
else:
    work_df[date_col] = pd.to_datetime(work_df[date_col], errors="coerce")
    by_date = (
        work_df.dropna(subset=[date_col])
        .groupby(work_df[date_col].dt.date, as_index=False)[sales_col]
        .sum()
        .rename(columns={date_col: "Ngày", sales_col: "Doanh số"})
    )

    if by_date.empty:
        st.warning("Cột ngày có dữ liệu không hợp lệ sau khi chuẩn hoá.")
    else:
        st.line_chart(by_date.set_index("Ngày")["Doanh số"], use_container_width=True)
        st.dataframe(by_date, use_container_width=True)

st.subheader("4) Doanh số theo ngành hàng")
category_col = pick_column(work_df, CATEGORY_CANDIDATES)
if category_col is None:
    st.info(
        "Không tìm thấy cột ngành hàng (ví dụ: 'Class', 'Dept.', 'Ngành hàng'). "
        "Đang hiển thị top theo 'Tên Hàng' nếu có."
    )
    fallback_col = "Tên Hàng" if "Tên Hàng" in work_df.columns else None
    if fallback_col is None:
        st.warning("Không có cột phù hợp để nhóm ngành hàng.")
    else:
        by_category = (
            work_df.groupby(fallback_col, as_index=False)[sales_col]
            .sum()
            .sort_values(by=sales_col, ascending=False)
            .head(20)
        )
        st.bar_chart(by_category.set_index(fallback_col)[sales_col], use_container_width=True)
        st.dataframe(by_category, use_container_width=True)
else:
    by_category = (
        work_df.groupby(category_col, as_index=False)[sales_col]
        .sum()
        .sort_values(by=sales_col, ascending=False)
    )
    st.bar_chart(by_category.set_index(category_col)[sales_col], use_container_width=True)
    st.dataframe(by_category, use_container_width=True)

st.caption(f"Đang dùng cột doanh số: '{sales_col}'.")
