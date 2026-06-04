import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Organization Registry",
    page_icon="🏢",
    layout="wide"
)

st.title("🏢 Organization Registry")

# Load data
df = pd.read_csv(
    "config/entity_registry.csv",
    encoding="utf-8-sig"
)

# KPIs
col1, col2, col3, col4 = st.columns(4)

col1.metric("Entities", len(df))
col2.metric("Countries", df["Country"].nunique())
col3.metric("Entity Types", df["Entity_Type"].nunique())
col4.metric("Sectors", df["Sector"].nunique())

st.divider()

# Search
search = st.text_input("🔍 Search Entity")

filtered = df.copy()

if search:
    filtered = filtered[
        filtered["Entity_Name"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

# Table
st.subheader("Registry")

st.dataframe(
    filtered,
    use_container_width=True
)

# Profile
if len(filtered) > 0:

    selected = st.selectbox(
        "Select Entity",
        filtered["Entity_Name"]
    )

    profile = filtered[
        filtered["Entity_Name"] == selected
    ].iloc[0]

    st.subheader("Entity Profile")

    st.write("**Entity Name:**", profile["Entity_Name"])
    st.write("**Entity Type:**", profile["Entity_Type"])
    st.write("**Country:**", profile["Country"])
    st.write("**Sector:**", profile["Sector"])
    st.write("**Industry:**", profile["Industry"])
    st.write("**Priority:**", profile["Priority"])
