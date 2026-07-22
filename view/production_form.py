import streamlit as st

from src.enum import ProductionStatus


def validate_number(str: str):
    if str.isdigit():
        validated_num = int(str)
        return validated_num
    else:
        st.error("Error: 숫자만 입력하세요.")


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

# 생산 등록 (> 생산 상태 변경: 진행 중) > 투입 원재료 등록 > 완제품 lot 등록 (> 생산 상태 변경: 완료)
