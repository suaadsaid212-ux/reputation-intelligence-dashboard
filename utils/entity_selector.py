import pandas as pd
import streamlit as st

def get_selected_entity():

    df = pd.read_csv(
        "config/entity_registry.csv"
    )

    selected = st.sidebar.selectbox(
        "Select Entity",
        df["Entity Name"]
    )

    entity = df[
        df["Entity Name"] == selected
    ].iloc[0]

    return entity
