import streamlit as st

from src.utils import connect_db
from src.enum import ProductType
from src.dto import ProductDto
from src.repository import ProductRepository


def handle_status():
    click = st.session_state.material_edit

    row_index = click["row"]
    selected_id = products[row_index].get("product_id")

    if selected_id:
        print(selected_id)


db = connect_db()

st.subheader("전체 제품 목록")

product_repository = ProductRepository(db)
products = product_repository.find_all()

# st.dataframe(
#     products,
#     column_config={
#         "product_id": "ID",
#         "product_code": "Code",
#         "product_name": "Name",
#         "product_type": "Type",
#         "is_active": "Status",
#     },
# )

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

if "products" in st.session_state:
    edited = st.session_state.products.get("edited_rows")

    if len(edited) > 0:
        for key, value in edited.items():
            # print(products[key].get("product_id"), value.get("is_active"))
            response = product_repository.update_product_status(
                value.get("is_active"), products[key].get("product_id")
            )

    st.session_state.pop("products")

st.divider()

with st.form(key="product", clear_on_submit=True):
    name = st.text_input("제품명")
    code = st.text_input("제품 코드")
    type = st.selectbox("제품 유형", ProductType)

    submitted = st.form_submit_button("제품 추가")

    if submitted:
        st.toast("제품이 추가되었습니다.")
        product = ProductDto(
            product_code=code, product_name=name, product_type=type, is_active=False
        )
        response = product_repository.add_product(product)

        if response:
            st.rerun()
