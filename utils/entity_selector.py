import streamlit as st
import pandas as pd

@st.cache_data
def load_registry():

```
return pd.read_csv(
    "config/entity_registry.csv",
    encoding="utf-8-sig"
)
```

def get_entity():

```
df = load_registry()

if df.empty:

    st.error(
        "Registry file is empty."
    )

    st.stop()

selected = st.sidebar.selectbox(
    "🏢 Select Entity",
    sorted(
        df["Entity_Name"]
        .dropna()
        .unique()
    )
)

entity = df[
    df["Entity_Name"] == selected
].iloc[0]

return entity
```
