import streamlit as st
from utils.entity_selector import get_selected_entity

st.title("🏢 Organization Registry")

entity = get_selected_entity()

st.write("Selected Entity")

st.dataframe(entity.to_frame())
