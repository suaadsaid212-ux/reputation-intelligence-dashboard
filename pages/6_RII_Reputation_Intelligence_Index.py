from utils.entity_selector import get_entity

# ====================================

# ENTITY SELECTION

# ====================================

entity = get_entity()

entity_name = entity["Entity_Name"]
entity_type = entity["Entity_Type"]
ticker = str(entity["Ticker"])

st.title("🏆 Reputation Intelligence Index (RII)")

st.markdown(f"""

### Reputation Risk Assessment

**Selected Entity:** {entity_name}

RII measures organizational reputation risk using:

* Exposure
* Vulnerability
* Resilience

Final Output:

Exposure + Vulnerability − Resilience
""")

# ====================================

# ENTITY PROFILE

# ====================================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
"Type",
entity["Entity_Type"]
)

c2.metric(
"Country",
entity["Country"]
)

c3.metric(
"Sector",
entity["Sector"]
)

c4.metric(
"Priority",
entity["Priority"]
)
