import streamlit as st
import pandas as pd

st.set_page_config(
page_title="Organization Registry",
page_icon="🏢",
layout="wide"
)

st.title("🏢 Organization Registry")

st.markdown("""
Central repository of organizations, governments,
universities, NGOs and international institutions
monitored by the Reputation Intelligence Platform.
""")

# =====================================

# LOAD REGISTRY

# =====================================

try:

```
df = pd.read_csv(
    "config/entity_registry.csv",
    encoding="utf-8-sig"
)
```

except Exception as e:

```
st.error("Unable to load entity_registry.csv")

st.code(str(e))

st.stop()
```

# =====================================

# OVERVIEW

# =====================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
"Total Entities",
len(df)
)

col2.metric(
"Countries",
df["Country"].nunique()
)

col3.metric(
"Sectors",
df["Sector"].nunique()
)

col4.metric(
"Entity Types",
df["Entity_Type"].nunique()
)

st.divider()

# =====================================

# FILTERS

# =====================================

c1, c2, c3 = st.columns(3)

with c1:

```
entity_type = st.selectbox(
    "Entity Type",
    ["All"] + sorted(
        df["Entity_Type"].dropna().unique()
    ).tolist()
)
```

with c2:

```
country = st.selectbox(
    "Country",
    ["All"] + sorted(
        df["Country"].dropna().unique()
    ).tolist()
)
```

with c3:

```
sector = st.selectbox(
    "Sector",
    ["All"] + sorted(
        df["Sector"].dropna().unique()
    ).tolist()
)
```

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

# =====================================

# SEARCH

# =====================================

search = st.text_input(
"🔍 Search Entity"
)

if search:

```
filtered = filtered[
    filtered["Entity_Name"].str.contains(
        search,
        case=False,
        na=False
    )
]
```

st.divider()

# =====================================

# REGISTRY TABLE

# =====================================

st.subheader("Registry")

st.dataframe(
filtered,
use_container_width=True
)

# =====================================

# ENTITY PROFILE

# =====================================

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

st.write("### Detailed Information")

st.json(
    profile.to_dict()
)
```
