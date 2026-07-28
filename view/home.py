import streamlit as st

st.header("MES")

st.page_link("view/product.py", label="생산 제품", icon=":material/save:")
st.page_link("view/material.py", label="원재료", icon=":material/save:")
st.page_link("view/production.py", label="생산 관리", icon=":material/monitoring:")
st.page_link(
    "view/production_form.py", label="생산 등록", icon=":material/open_in_new:"
)
