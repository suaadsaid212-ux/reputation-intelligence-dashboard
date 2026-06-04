import streamlit as st
import pandas as pd

st.set_page_config(
page_title="Organization Registry",
layout="wide"
)

st.title("🏢 Organization Registry")

# ====================================

# LOAD CSV SAFELY

# ====================================

try:

```
df = pd.read_csv(
    "config/entity_registry.csv",
    encoding="utf-8-sig"
)
```

except Exception as e:

```
st.error("CSV Error Detected")

st.code(str(e))

st.info(
    """
    Your entity_registry.csv contains a formatting issue.

    Common causes:

    • Missing comma
    • Extra comma
    • Different number of columns
    • Broken row
    """
)

st.stop()
```

# ====================================

# SHOW BASIC INFO

# ====================================

st.success(
f"Registry Loaded Successfully ({len(df)} Entities)"
)

st.subheader("Preview")

st.dataframe(
df.head(20),
use_container_width=True
)

# ====================================

# FILTERS

# ====================================

col1, col2, col3 = st.columns(3)

with col1:

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

with col2:

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

with col3:

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

# ====================================

# SEARCH

# ====================================

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

# ====================================

# REGISTRY TABLE

# ====================================

st.subheader("Registry")

st.dataframe(
filtered,
use_container_width=True
)

# ====================================

# PROFILE

# ====================================

if len(filtered) > 0:

```
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
    "Type",
    str(profile["Entity_Type"])
)

c2.metric(
    "Country",
    str(profile["Country"])
)

c3.metric(
    "Sector",
    str(profile["Sector"])
)

c4.metric(
    "Priority",
    str(profile["Priority"])
)

st.write("### Details")

st.json(
    profile.to_dict()
)
```
