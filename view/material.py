import streamlit as st

from src.database import Database
from src.repository import MaterialRepository
from src.dto import MaterialDto
from src.enum import MaterialCategory

st.subheader("원재료 목록")

try:
    with Database() as db:
        material_repository = MaterialRepository(db)
        material = material_repository.find_all()

        st.dataframe(material)


except RuntimeError as e:
    print(e)
    st.error("조회 가능한 제품이 없습니다.")

st.divider()

with st.form(key="material", clear_on_submit=True):
    name = st.text_input("원재료명")
    code = st.text_input("원재료 코드")
    category = st.selectbox("카테고리", MaterialCategory)

    submitted = st.form_submit_button("재료 추가")

    if submitted:
        st.toast("원재료가 추가되었습니다.")
