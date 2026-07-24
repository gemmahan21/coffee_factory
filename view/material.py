import streamlit as st

from src.utils import connect_db
from src.enum import MaterialCategory
from src.repository import MaterialRepository

db = connect_db()

st.subheader("원재료 목록")

material_repository = MaterialRepository(db)
material = material_repository.find_all()

st.dataframe(material)

st.divider()

with st.form(key="material", clear_on_submit=True):
    name = st.text_input("원재료명")
    code = st.text_input("원재료 코드")
    category = st.selectbox("카테고리", MaterialCategory)

    submitted = st.form_submit_button("재료 추가")

    if submitted:
        st.toast("원재료가 추가되었습니다.")
