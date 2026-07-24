import streamlit as st

from src.enum import ProductionStatus
from src.utils import validate_number

st.subheader("생산 등록")
with st.form(key="production", clear_on_submit=True):
    code = st.text_input("생산 Code")
    product_id = st.text_input("제품 ID")
    quantity = st.text_input("수량")
    unit = st.text_input("단위", value="EA")
    status = st.selectbox("생산 상태", ProductionStatus)

    submitted = st.form_submit_button("추가")

    if submitted:
        product_id = validate_number(product_id)
        quantity = validate_number(quantity)

        if product_id < 1:
            st.error("제품 ID 숫자를 입력하세요.")
        if quantity < 1:
            st.error("수량에는 숫자만 입력하세요.")

        st.success(code)

# 생산 등록 (> 생산 상태 변경: 진행 중) > 투입 원재료 등록 > 완제품 lot 등록 (> 생산 상태 변경: 완료)
