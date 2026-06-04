import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Organization Registry",
    layout="wide"
)

st.title("🏢 Organization Registry")

# Load CSV

try:
    df = pd.read_csv(
        "config/entity_registry.csv",
        encoding="utf-8-sig"
    )

except Exception as e:

    st.error("CSV Error")

    st.code(str(e))

    st.stop()

# Show success

st.success(
    f"Loaded {len(df)} entities successfully"
)

# Filters

col1, col2, col3 = st.columns(3)

with col1:
    entity_type = st.selectbox(
        "Entity Type",
        ["All"] + sorted(
            df["Entity_Type"].dropna().unique().tolist()
        )
    )

with col2:
    country = st.selectbox(
        "Country",
        ["All"] + sorted(
            df["Country"].dropna().unique().tolist()
        )
    )

with col3:
    sector = st.selectbox(
        "Sector",
        ["All"] + sorted(
            df["Sector"].dropna().unique().tolist()
        )
    )

filtered = df.copy()

if entity_type != "All":
    filtered = filtered[
        filtered["Entity_Type"] == entity_type
    ]

if country != "All":
    filtered = filtered[
        filtered["Country"] == country
    ]

if sector != "All":
    filtered = filtered[
        filtered["Sector"] == sector
    ]

# Search

search = st.text_input(
    "🔍 Search Entity"
)

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

if not filtered.empty:

    selected = st.selectbox(
        "Select Entity",
        filtered["Entity_Name"]
    )

    profile = filtered[
        filtered["Entity_Name"] == selected
    ].iloc[0]

    st.subheader("Entity Profile")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Type",
        profile["Entity_Type"]
    )

    col2.metric(
        "Country",
        profile["Country"]
    )

    col3.metric(
        "Sector",
        profile["Sector"]
    )

    col4.metric(
        "Priority",
        profile["Priority"]
    )

    st.write("### Details")

    st.json(
        profile.to_dict()
    )
