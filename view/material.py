import streamlit as st

from src.utils import connect_db
from src.enum import MaterialCategory
from src.repository import MaterialRepository
from src.dto import MaterialDto


def on_click_edit():
    click = st.session_state.material_edit

    row_index = click["row"]
    selected_id = materials[row_index].get("material_id")

    if selected_id:
        material_repository.remove_material(selected_id)


db = connect_db()

st.subheader("원재료 목록")

material_repository = MaterialRepository(db)
materials = material_repository.find_all()

for material in materials:
    material["edit"] = ":material/delete:"

st.dataframe(
    materials,
    column_config={
        "edit": st.column_config.ButtonColumn(
            type="secondary", on_click=on_click_edit, key="material_edit", label=""
        )
    },
)


st.divider()

with st.form(key="material", clear_on_submit=True):
    name = st.text_input("원재료명")
    code = st.text_input("원재료 코드")
    category = st.selectbox("카테고리", MaterialCategory)

    submitted = st.form_submit_button("재료 추가")

    if submitted:
        new_material = MaterialDto(
            material_code=code, material_name=name, category=category
        )
        response = material_repository.add_material(new_material)

        if response:
            st.rerun()
