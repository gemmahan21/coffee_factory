import streamlit as st

from src.utils import connect_db, generate_product_code
from src.enum import ProductType
from src.dto import ProductDto
from src.repository import ProductRepository, ProductionRepository

st.markdown(
    """
    <style>
    [data-testid="stMetric"] {
        min-width: 132px;
    }
    [data-testid="stMetricLabel"] {
        font-size: 8px;
        border-bottom: 1px solid #ddd;
    }
    [data-testid="stMetricValue"] {
        font-size: 16px;
        font-weight: bold;
        margin: 8px 0 3px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def update_product_code_input():
    product_type = st.session_state.product_type
    st.session_state.product_code = generate_product_code(product_type)


db = connect_db()

st.subheader("전체 제품 목록")

product_repository = ProductRepository(db)
products = product_repository.find_all()

production_repository = ProductionRepository(db)
quantity = production_repository.production_quantity_by_product()

st.markdown("##### 제품별 총 생산량\n")

if len(quantity) < 6:
    cols = st.columns(len(quantity))

    for col, temp in zip(cols, quantity):
        with col:
            st.metric(
                label="".join((temp.get("product_name").replace("커피", "")).split()),
                value=temp.get("sum"),
                delta="총 생산량",
                delta_arrow="off",
                border=True,
                format="localized",
            )
else:
    st.dataframe(
        quantity,
        column_config={
            "product_id": None,
            "product_name": "Name",
            "sum": "Total Quantity",
        },
    )


st.divider()

active_count = product_repository.get_count_by_is_active(True)
st.info(f"현재 생산 중인 제품 개수 : {active_count}")

st.data_editor(
    products,
    column_config={
        "product_id": "ID",
        "product_code": "Code",
        "product_name": "Name",
        "product_type": "Type",
        "is_active": "Status",
    },
    key="products",
    disabled=["product_id", "product_code", "product_name", "product_type"],
)

if st.button("제품 상태 업데이트"):
    if "products" in st.session_state:
        edited = st.session_state.products.get("edited_rows")

        if len(edited) > 0:
            for key, value in edited.items():
                # print(products[key].get("product_id"), value.get("is_active"))
                response = product_repository.update_product_status(
                    value.get("is_active"), products[key].get("product_id")
                )

            st.toast("상태가 변경되었습니다.")
        else:
            st.toast("변경 내역이 없습니다.")

        st.session_state.pop("products")

st.divider()

with st.container(border=True):
    type = st.selectbox(
        "제품 유형",
        ProductType,
        key="product_type",
        on_change=update_product_code_input,
    )

    if "product_code" not in st.session_state:
        st.session_state.product_code = f"{generate_product_code(type)}"

    with st.form(key="product", border=False, clear_on_submit=True):
        name = st.text_input("제품명")
        code = st.text_input("제품 코드", key="product_code")

        submitted = st.form_submit_button("제품 추가")

        if submitted:
            st.toast("제품이 추가되었습니다.")
            product = ProductDto(
                product_code=code, product_name=name, product_type=type, is_active=False
            )
            response = product_repository.add_product(product)

            if response:
                st.rerun()
