import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Organization Registry",
    layout="wide"
)

st.title("🏢 Organization Registry")

df = pd.read_csv(
    "config/entity_registry.csv"
)

st.success(
    f"Loaded {len(df)} entities successfully"
)

st.dataframe(
    df,
    use_container_width=True
)
