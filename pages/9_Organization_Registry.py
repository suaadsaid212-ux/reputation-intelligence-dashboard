import streamlit as st
import pandas as pd

st.set_page_config(
page_title="Organization Registry",
page_icon="🏢",
layout="wide"
)

# ==========================================

# LOAD DATA

# ==========================================

df = pd.read_csv(
"config/entity_registry.csv",
encoding="utf-8-sig"
)

# ==========================================

# PAGE TITLE

# ==========================================

st.title("🏢 Organization Registry")

st.markdown("""
Central repository of organizations, governments,
universities, international organizations and companies
monitored by the Reputation Intelligence Platform.
""")

# ==========================================

# KPI CARDS

# ==========================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
"Entities",
len(df)
)

col2.metric(
"Countries",
df["Country"].nunique()
)

col3.metric(
"Entity Types",
df["Entity_Type"].nunique()
)

col4.metric(
"Sectors",
df["Sector"].nunique()
)

st.divider()

# ==========================================

# FILTERS

# ==========================================

f1, f2, f3 = st.columns(3)

with f1:

```
entity_type = st.selectbox(
    "Entity Type",
    ["All"] +
    sorted(
        df["Entity_Type"]
        .dropna()
        .unique()
        .tolist()
    )
)
```

with f2:

```
country = st.selectbox(
    "Country",
    ["All"] +
    sorted(
        df["Country"]
        .dropna()
        .unique()
        .tolist()
    )
)
```

with f3:

```
sector = st.selectbox(
    "Sector",
    ["All"] +
    sorted(
        df["Sector"]
        .dropna()
        .unique()
        .tolist()
    )
)
```

# ==========================================

# APPLY FILTERS

# ==========================================

filtered = df.copy()

if entity_type != "All":

```
filtered = filtered[
    filtered["Entity_Type"] == entity_type
]
```

if country != "All":

```
filtered = filtered[
    filtered["Country"] == country
]
```

if sector != "All":

```
filtered = filtered[
    filtered["Sector"] == sector
]
```

# ==========================================

# SEARCH

# ==========================================

search = st.text_input(
"🔍 Search Entity"
)

if search:

```
filtered = filtered[
    filtered["Entity_Name"]
    .str.contains(
        search,
        case=False,
        na=False
    )
]
```

st.divider()

# ==========================================

# REGISTRY TABLE

# ==========================================

st.subheader("Registry")

st.dataframe(
filtered,
use_container_width=True,
height=450
)

# ==========================================

# ENTITY PROFILE

# ==========================================

if not filtered.empty:

```
selected = st.selectbox(
    "Select Entity",
    filtered["Entity_Name"]
)

profile = filtered[
    filtered["Entity_Name"] == selected
].iloc[0]

st.divider()

st.subheader("📋 Entity Profile")

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

st.markdown("### Details")

details = pd.DataFrame({
    "Attribute": [
        "Entity ID",
        "Entity Name",
        "Short Name",
        "Entity Type",
        "Ticker",
        "Country",
        "Sector",
        "Industry",
        "Data Source Type",
        "Priority"
    ],
    "Value": [
        profile["Entity_ID"],
        profile["Entity_Name"],
        profile["Short_Name"],
        profile["Entity_Type"],
        profile["Ticker"],
        profile["Country"],
        profile["Sector"],
        profile["Industry"],
        profile["Data_Source_Type"],
        profile["Priority"]
    ]
})

st.dataframe(
    details,
    use_container_width=True,
    hide_index=True
)
```

# ==========================================

# COUNTRY SUMMARY

# ==========================================

st.divider()

st.subheader("🌍 Country Distribution")

country_summary = (
df["Country"]
.value_counts()
.reset_index()
)

country_summary.columns = [
"Country",
"Entities"
]

st.dataframe(
country_summary,
use_container_width=True
)

# ==========================================

# ENTITY TYPE SUMMARY

# ==========================================

st.subheader("🏷️ Entity Type Distribution")

type_summary = (
df["Entity_Type"]
.value_counts()
.reset_index()
)

type_summary.columns = [
"Entity Type",
"Count"
]

st.dataframe(
type_summary,
use_container_width=True
)

# ==========================================

# WATCHLIST

# ==========================================

st.divider()

st.subheader("⭐ Watchlist")

watchlist = st.multiselect(
"Select Strategic Entities",
df["Entity_Name"].tolist()
)

if watchlist:

```
watch_df = df[
    df["Entity_Name"].isin(
        watchlist
    )
]

st.dataframe(
    watch_df,
    use_container_width=True
)
```
