import streamlit as st

from src.utils import connect_db, genarate_material_code
from src.enum import MaterialCategory
from src.repository import MaterialRepository
from src.dto import MaterialDto


@st.dialog("등록된 원재료 지우기")
def confirm_delete(selected: int):
    st.write("정말 삭제하시겠습니까?")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes"):
            st.session_state.confirm = True
            material_repository.remove_material(selected)
    with col2:
        if st.button("No"):
            st.session_state.confirm = False

    del st.session_state["confirm"]
    st.rerun()


def on_edit():
    click = st.session_state.material_edit

    row_index = click["row"]
    selected_id = materials[row_index].get("material_id")

    if selected_id:
        # material_repository.remove_material(selected_id)
        if "confirm" not in st.session_state:
            st.session_state.confirm = False

        confirm_delete(selected=selected_id)


def update_material_code_input():
    material_category = st.session_state.material_category
    st.session_state.material_code = genarate_material_code(material_category)


db = connect_db()

st.subheader("원재료 목록")

material_repository = MaterialRepository(db)
materials = material_repository.find_all()

for material in materials:
    material["edit"] = ":material/delete:"

st.dataframe(
    materials,
    column_config={
        "material_id": "ID",
        "material_code": "Code",
        "material_name": "Name",
        "category": "Category",
        "edit": st.column_config.ButtonColumn(
            type="secondary",
            on_click=on_edit,
            key="material_edit",
            label="",
        ),
    },
)


st.divider()

with st.container(border=True):
    category = st.selectbox(
        "카테고리",
        MaterialCategory,
        key="material_category",
        on_change=update_material_code_input,
    )

    if "material_code" not in st.session_state:
        st.session_state.material_code = f"{genarate_material_code(category)}"

    with st.form(key="material", border=False, clear_on_submit=True):
        name = st.text_input("원재료명")
        code = st.text_input("원재료 코드", key="material_code")

        submitted = st.form_submit_button("재료 추가")

        if submitted:
            new_material = MaterialDto(
                material_code=code, material_name=name, category=category
            )
            response = material_repository.add_material(new_material)

            if response:
                st.rerun()
