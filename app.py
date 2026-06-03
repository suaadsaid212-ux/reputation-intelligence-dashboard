import streamlit as st

st.set_page_config(
    page_title="Reputation Intelligence Platform",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Reputation Intelligence Platform")

st.markdown("""
### AI-Powered Reputation Risk Monitoring System

Monitor organizations, countries, narratives, market sentiment,
search behavior, financial volatility, and reputation risk in real time.
""")

st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Organizations",
        "3",
        "Tesla, Microsoft, Nestlé"
    )

with col2:
    st.metric(
        "Countries",
        "195",
        "Global Coverage"
    )

with col3:
    st.metric(
        "Intelligence Pages",
        "8",
        "Active"
    )

with col4:
    st.metric(
        "Data Sources",
        "5",
        "News, Finance, Trends"
    )

st.divider()

st.subheader("Platform Modules")

modules = [
    "Executive Overview",
    "Organization Intelligence",
    "Country Exposure",
    "Narrative Intelligence",
    "Sentiment & Subjectivity",
    "NRRI Risk Index",
    "Google Trends Intelligence",
    "Reputation Intelligence Index (RII)"
]

for module in modules:
    st.write("✅", module)

st.divider()

st.subheader("Current Benchmark Organizations")

benchmark_data = {
    "Tesla": "High Disinformation Exposure",
    "Microsoft": "Digital Trust & AI Leadership",
    "Nestlé": "Global Consumer Reputation"
}

for org, desc in benchmark_data.items():
    st.info(f"**{org}** — {desc}")

st.divider()

st.subheader("Platform Roadmap")

st.write("""
**Current Version**
- News Intelligence
- Sentiment Analysis
- Subjectivity Analysis
- Google Trends
- RII Scoring

**Next Releases**
- Organization Registry
- Lifecycle Intelligence
- Crisis Early Warning
- Reputation Forecasting
- Global Risk Map
- Competitive Benchmarking
""")

st.success("Platform Status: Operational")
