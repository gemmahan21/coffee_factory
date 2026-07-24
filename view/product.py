import streamlit as st

from src.utils import connect_db
from src.enum import ProductType
from src.repository import ProductRepository

db = connect_db()

st.subheader("전체 제품 목록")

product_repository = ProductRepository(db)
products = product_repository.find_all()

st.dataframe(
    products,
    column_config={
        "product_id": "ID",
        "product_code": "Code",
        "product_name": "Name",
        "product_type": "Type",
        "is_active": "Status",
    },
)

st.divider()

with st.form(key="product", clear_on_submit=True):
    name = st.text_input("제품명")
    code = st.text_input("제품 코드")
    type = st.selectbox("제품 유형", ProductType)

    submitted = st.form_submit_button("제품 추가")

    if submitted:
        st.toast("제품이 추가되었습니다.")
        # product = ProductDto(code, name, type)
        # product_repository.add_product(product)
