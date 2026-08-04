import streamlit as st
import pandas as pd

from src.utils import (
    connect_db,
    validate_number,
    input_production_material,
    create_product_lot,
    get_current_date,
    generate_code,
)
from src.repository import ProductionRepository
from src.enum import ProductionStatus
from src.dto import ProductionMaterialDto, ProductLotDto

st.set_page_config(layout="wide")


def add_input_material():
    st.session_state.input_material_count += 1


def remove_input_material():
    if st.session_state.input_material_count > 1:
        last_index = st.session_state.input_material_count - 1

        st.session_state.pop(f"input_material_id_{last_index}", None)
        st.session_state.pop(f"input_material_quantity_{last_index}", None)
        st.session_state.pop(f"input_material_unit_{last_index}", None)

        st.session_state.input_material_count -= 1


db = connect_db()
production_repository = ProductionRepository(db)

st.header("제품 생산 관리")

st.markdown("#### 생산 목록")

production = production_repository.find_all_production()
st.dataframe(production, width="stretch")

column1, column2 = st.columns(2, gap="large")

with column1:
    tab1, tab2 = st.tabs(["생산 차트", "생산 조회"])

    with tab1:
        current_date = get_current_date()

        st.markdown("##### 최근 생산량")
        col1, col2 = st.columns(2)
        with col1:
            start = st.date_input("Start", value=current_date.get("start"))
        with col2:
            end = st.date_input("End", max_value="today")

        production_quantity = production_repository.get_quantity_by_date(
            start=start, end=end
        )
        quantity_df = pd.DataFrame(production_quantity)
        st.bar_chart(
            quantity_df,
            x="produced_at",
            y="quantity",
            x_label="생산일",
            y_label="생산량",
        )

    with tab2:
        st.markdown("##### 생산 Lot으로 제품 조회")

        with st.form(key="product_lot_search", clear_on_submit=True, border=False):
            lot_no = st.text_input("Lot 번호", value="LOT-FG-")

            submitted = st.form_submit_button("검색")

            if submitted:
                product = production_repository.find_product_by_product_lot(lot_no)
                if product is None:
                    st.write("생산 내역이 없습니다.")
                else:
                    st.dataframe(product)

        st.divider()

        st.markdown("##### 투입 원재료 조회")

        with st.form(key="input_material", clear_on_submit=True, border=False):
            production_id = st.text_input("생산 ID")

            submitted = st.form_submit_button("검색")

            if submitted:
                input_material = (
                    production_repository.find_input_material_by_production(
                        production_id
                    )
                )
                if len(input_material) < 1:
                    st.write("생산 내역이 없습니다.")
                else:
                    st.dataframe(input_material)

with column2:
    st.markdown("#### 생산 관리\n")
    st.markdown("##### 생산 상태 변경")
    with st.form(key="production_status", clear_on_submit=True):
        production_id = st.text_input("생산 ID")
        status = st.selectbox("Status", ProductionStatus)

        submitted = st.form_submit_button("변경")
        if submitted:
            response = production_repository.update_production_status(
                production_id, status
            )
            if response:
                st.rerun()

    st.markdown("##### 투입 원재료 등록")
    with st.container(border=True):
        production_id = st.text_input("생산 ID")  # status: progress

        if "input_material_count" not in st.session_state:
            st.session_state.input_material_count = 1

        btn1, btn2 = st.columns(2)
        with btn1:
            st.button(
                "+ 항목 추가", on_click=add_input_material, use_container_width=True
            )
        with btn2:
            st.button(
                "- 항목 삭제", on_click=remove_input_material, use_container_width=True
            )

        with st.form(key="production_material", border=False, clear_on_submit=True):
            for i in range(st.session_state.input_material_count):
                st.divider()
                material_id = st.text_input("원재료 ID", key=f"input_material_id_{i}")
                quantity = st.text_input("수량", key=f"input_material_quantity_{i}")
                unit = st.selectbox(
                    "단위", ["EA", "Box"], key=f"input_material_unit_{i}"
                )

            submitted = st.form_submit_button("등록")

            if submitted:
                count = 1
                if st.session_state.input_material_count > 0:
                    count = st.session_state.input_material_count

                for i in range(count):
                    material_id = st.session_state.get(f"input_material_id_{i}")
                    quantity = st.session_state.get(f"input_material_quantity_{i}")
                    unit = st.session_state.get(f"input_material_unit_{i}")

                    quantity = validate_number(quantity)
                    if quantity < 1:
                        st.error("수량에는 숫자만 입력하세요.")
                        break
                    else:
                        production_material = ProductionMaterialDto(
                            production_id=production_id,
                            material_id=material_id,
                            quantity=quantity,
                            unit=unit,
                        )
                        response = input_production_material(
                            production_repository, production_material
                        )
                        if response:
                            # print(response)
                            st.toast("원재료가 등록되었습니다.")
                        else:
                            st.toast("생산 상태가 진행 중인지 확인하세요.")
                            break

                st.session_state.input_material_count = 1

    st.markdown("##### 생산 Lot 등록")
    with st.form(key="product_lot", clear_on_submit=True):
        production_id = st.text_input("생산 ID")  # status: complete
        lot_no = st.text_input("Lot 번호", value=f"{generate_code("product_lot")}")

        submitted = st.form_submit_button("등록")

        if submitted:
            product_lot = ProductLotDto(lot_no=lot_no, production_id=production_id)
            response = create_product_lot(production_repository, product_lot)
            if response:
                # print(response)
                st.toast("생산 Lot이 등록되었습니다.")
            else:
                st.toast("생산 상태가 완료되었는지 확인하세요.")
