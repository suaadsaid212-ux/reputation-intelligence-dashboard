import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="Sector Intelligence",
    page_icon="🏭",
    layout="wide",
)

st.title("🏭 Sector Intelligence")

st.markdown("""
Compare organizations within the same sector and identify:

- Sector Leaders
- Highest Risk Entities
- Fastest Growing Entities
- Reputation Outliers
- Competitive Positioning
""")

df = pd.read_csv(
    "config/entity_registry.csv",
    encoding="utf-8-sig",
)

sector = st.selectbox(
    "Select Sector",
    sorted(
        df["Sector"]
        .dropna()
        .unique()
        .tolist()
    ),
)

sector_df = df[df["Sector"] == sector]

if sector_df.empty:
    st.warning("No entities found for this sector.")
    st.stop()

benchmark = []

for _, row in sector_df.iterrows():
    benchmark.append({
        "Entity": row["Entity_Name"],
        "RII": np.random.randint(30, 95),
        "OLI": np.random.randint(30, 95),
        "Search": np.random.randint(30, 95),
        "Social": np.random.randint(30, 95),
        "Crisis": np.random.randint(10, 90),
    })

benchmark_df = pd.DataFrame(benchmark)

st.subheader("Sector Overview")

k1, k2, k3, k4 = st.columns(4)

k1.metric("Entities", len(benchmark_df))
k2.metric("Avg RII", round(benchmark_df["RII"].mean(), 1))
k3.metric("Avg OLI", round(benchmark_df["OLI"].mean(), 1))
k4.metric("Avg Crisis", round(benchmark_df["Crisis"].mean(), 1))

st.subheader("Sector Benchmark")

st.dataframe(benchmark_df, use_container_width=True)

st.subheader("Sector Ranking")

ranking = benchmark_df.copy()

ranking["Composite Score"] = (
    ranking["RII"] * 0.30
    + ranking["OLI"] * 0.30
    + ranking["Search"] * 0.20
    + ranking["Social"] * 0.20
)

ranking = ranking.sort_values(
    by="Composite Score",
    ascending=False,
)

st.dataframe(
    ranking[
        [
            "Entity",
            "Composite Score",
        ]
    ],
    use_container_width=True,
)

st.subheader("Entity Comparison")

entities = st.multiselect(
    "Select Entities",
    benchmark_df["Entity"].tolist(),
    default=benchmark_df["Entity"].head(3).tolist(),
)

radar = go.Figure()

for entity in entities:
    row = benchmark_df[
        benchmark_df["Entity"] == entity
    ].iloc[0]

    radar.add_trace(
        go.Scatterpolar(
            r=[
                row["RII"],
                row["OLI"],
                row["Search"],
                row["Social"],
                row["Crisis"],
            ],
            theta=[
                "RII",
                "OLI",
                "Search",
                "Social",
                "Crisis",
            ],
            fill="toself",
            name=entity,
        )
    )

radar.update_layout(
    height=650,
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 100],
        )
    ),
)

st.plotly_chart(radar, use_container_width=True)

st.subheader("Competitive Position Matrix")

matrix = go.Figure()

matrix.add_trace(
    go.Scatter(
        x=benchmark_df["Search"],
        y=benchmark_df["RII"],
        mode="markers+text",
        text=benchmark_df["Entity"],
        textposition="top center",
    )
)

matrix.update_layout(
    xaxis_title="Visibility",
    yaxis_title="Reputation",
    height=600,
)

st.plotly_chart(matrix, use_container_width=True)

st.subheader("Executive Insights")

leader = ranking.iloc[0]

highest_risk = benchmark_df.sort_values(
    by="Crisis",
    ascending=False,
).iloc[0]

st.success(f"Sector Leader: {leader['Entity']}")
st.warning(f"Highest Crisis Exposure: {highest_risk['Entity']}")

st.info("""
Future versions will calculate:

- Real RII
- Real OLI
- Real Search Intelligence
- Real Social Intelligence

instead of simulated benchmark scores.
""")
