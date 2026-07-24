import streamlit as st

from src.utils import connect_db
from src.repository import ProductionRepository
from src.service import ProductionService

db = connect_db()
production_repository = ProductionRepository(db)
production_service = ProductionService(production_repository)

st.header("제품 생산 관리")

st.subheader("생산 목록")

production = production_service.find_all_production()
st.dataframe(production)

tab1, tab2 = st.tabs(["생산 조회", "생산 관리"])

with tab1:
    st.subheader("생산 Lot으로 제품 조회")

    with st.form(key="product_lot_search", clear_on_submit=True, border=False):
        lot_no = st.text_input("Lot 번호")

        submitted = st.form_submit_button("검색")

        if submitted:
            products = production_service.find_product_by_product_lot(lot_no)
            st.dataframe(products)

    st.divider()

    st.subheader("생산에 투입된 원재료 조회")

    with st.form(key="input_material", clear_on_submit=True, border=False):
        production_id = st.text_input("생산 ID")

        submitted = st.form_submit_button("검색")

        if submitted:
            input_material = production_service.find_input_material_by_production(
                production_id
            )
            st.dataframe(input_material)

with tab2:
    st.subheader("투입 원재료 등록")
    with st.form(key="production_material", clear_on_submit=True):
        production_id = st.text_input("생산 ID")  # status: progress
        material_id = st.text_input("원재료 ID")
        quantity = st.text_input("수량")
        unit = st.text_input("단위", value="EA")

        submitted = st.form_submit_button("등록")

    st.subheader("생산 Lot 등록")
    with st.form(key="product_lot", clear_on_submit=True):
        production_id = st.text_input("생산 ID")  # status: complete
        lot_no = st.text_input("Lot 번호")

        submitted = st.form_submit_button("등록")
