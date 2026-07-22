import streamlit as st

st.header("MES")

st.page_link("view/product.py", label="생산 제품", icon=":material/settings:")
st.page_link("view/material.py", label="원재료", icon=":material/settings:")
st.page_link("view/production.py", label="생산 관리", icon=":material/search:")
