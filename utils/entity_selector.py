import streamlit as st
import pandas as pd

@st.cache_data
def load_registry():

    return pd.read_csv(
        "config/entity_registry.csv",
        encoding="utf-8-sig"
    )

def get_entity():

    df = load_registry()

    selected = st.sidebar.selectbox(
        "🏢 Select Entity",
        df["Entity_Name"]
    )

    entity = df[
        df["Entity_Name"] == selected
    ].iloc[0]

    return entity
