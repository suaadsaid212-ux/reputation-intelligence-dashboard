import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Organization Registry",
    layout="wide"
)

st.title("🏢 Organization Registry")

# Load Registry

df = pd.read_csv(
    "config/entity_registry.csv"
)

# ====================================
# FILTERS
# ====================================

col1, col2, col3 = st.columns(3)

with col1:
    entity_type = st.selectbox(
        "Entity Type",
        ["All"] + sorted(df["Entity_Type"].dropna().unique())
    )

with col2:
    country = st.selectbox(
        "Country",
        ["All"] + sorted(df["Country"].dropna().unique())
    )

with col3:
    sector = st.selectbox(
        "Sector",
        ["All"] + sorted(df["Sector"].dropna().unique())
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

# ====================================
# SEARCH
# ====================================

search = st.text_input(
    "🔍 Search Entity"
)

if search:

    filtered = filtered[
        filtered["Entity_Name"]
        .str.contains(search, case=False, na=False)
    ]

# ====================================
# REGISTRY TABLE
# ====================================

st.subheader("Registry")

st.dataframe(
    filtered,
    use_container_width=True
)

# ====================================
# ENTITY PROFILE
# ====================================

if not filtered.empty:

    selected = st.selectbox(
        "Select Entity",
        filtered["Entity_Name"]
    )

    profile = filtered[
        filtered["Entity_Name"] == selected
    ].iloc[0]

    st.subheader("Entity Profile")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Entity Type",
        profile["Entity_Type"]
    )

    c2.metric(
        "Country",
        profile["Country"]
    )

    c3.metric(
        "Sector",
        profile["Sector"]
    )

    c4.metric(
        "Priority",
        profile["Priority"]
    )

    st.info(
        f"""
        Name: {profile['Entity_Name']}

        Short Name: {profile['Short_Name']}

        Industry: {profile['Industry']}

        Data Source Type: {profile['Data_Source_Type']}
        """
    )
