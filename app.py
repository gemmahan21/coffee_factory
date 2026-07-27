import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(layout="centered")

home = st.Page("view/home.py", title="Main")
product = st.Page("view/product.py", title="생산 제품")
material = st.Page("view/material.py", title="원재료")
production = st.Page("view/production.py", title="제품 생산 관리")
production_form = st.Page("view/production_form.py", title="생산 등록")

pages = st.navigation(
    {
        "MES": [home, product, material, production, production_form],
    }
)

pages.run()
