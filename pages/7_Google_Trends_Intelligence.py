import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pytrends.request import TrendReq

st.set_page_config(
    page_title="Google Trends Intelligence",
    layout="wide"
)

st.title("Google Trends Intelligence")

st.write(
    "This page analyzes public search interest, search momentum, "
    "search volatility, and geographic search exposure."
)

company_input = st.sidebar.text_input(
    "Enter company names or tickers",
    "Tesla, Microsoft, Meta"
)

timeframe = st.sidebar.selectbox(
    "Google Trends Period",
    [
        "today 1-m",
        "today 3-m",
        "today 12-m",
        "today 5-y"
    ]
)

geo = st.sidebar.text_input(
    "Country code, optional",
    ""
)

companies = [
    c.strip()
    for c in company_input.split(",")
    if c.strip() != ""
]

pytrends = TrendReq(
    hl="en-US",
    tz=360
)

try:
    pytrends.build_payload(
        companies,
        cat=0,
        timeframe=timeframe,
        geo=geo,
        gprop=""
    )

    trends_df = pytrends.interest_over_time()

except Exception as e:
    st.error(f"Google Trends data could not be loaded: {e}")
    st.stop()

if trends_df.empty:
    st.error("No Google Trends data found.")
    st.stop()

if "isPartial" in trends_df.columns:
    trends_df = trends_df.drop(columns=["isPartial"])

st.subheader("Search Interest Timeline")

fig = go.Figure()

for company in companies:

    if company in trends_df.columns:

        fig.add_trace(
            go.Scatter(
                x=trends_df.index,
                y=trends_df[company],
                mode="lines",
                name=company
            )
        )

fig.update_layout(
    template="plotly_dark",
    height=600,
    xaxis_title="Date",
    yaxis_title="Search Interest"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

summary_rows = []

for company in companies:

    if company not in trends_df.columns:
        continue

    series = trends_df[company]

    avg_interest = series.mean()
    max_interest = series.max()
    volatility = series.std()

    first_value = series.iloc[0]
    last_value = series.iloc[-1]

    if first_value == 0:
        momentum = 0
    else:
        momentum = (
            (last_value - first_value)
            / first_value
        ) * 100

    search_risk_index = (
        (0.40 * avg_interest) +
        (0.35 * volatility) +
        (0.25 * abs(momentum))
    )

    summary_rows.append({
        "Company": company,
        "Average Search Interest": round(float(avg_interest), 2),
        "Maximum Search Interest": round(float(max_interest), 2),
        "Search Volatility": round(float(volatility), 2),
        "Search Momentum %": round(float(momentum), 2),
        "Search Risk Index": round(float(search_risk_index), 2)
    })

summary_df = pd.DataFrame(summary_rows)

st.subheader("Search Intelligence Summary")

st.dataframe(
    summary_df,
    use_container_width=True
)

st.subheader("Search Risk Index Ranking")

ranking_df = summary_df.sort_values(
    by="Search Risk Index",
    ascending=False
)

ranking_fig = go.Figure()

ranking_fig.add_trace(
    go.Bar(
        x=ranking_df["Company"],
        y=ranking_df["Search Risk Index"],
        text=ranking_df["Search Risk Index"],
        textposition="auto"
    )
)

ranking_fig.update_layout(
    template="plotly_dark",
    height=500,
    yaxis_title="Search Risk Index"
)

st.plotly_chart(
    ranking_fig,
    use_container_width=True
)

st.subheader("Search Volatility Comparison")

vol_fig = go.Figure()

vol_fig.add_trace(
    go.Bar(
        x=summary_df["Company"],
        y=summary_df["Search Volatility"],
        text=summary_df["Search Volatility"],
        textposition="auto"
    )
)

vol_fig.update_layout(
    template="plotly_dark",
    height=500,
    yaxis_title="Search Volatility"
)

st.plotly_chart(
    vol_fig,
    use_container_width=True
)

st.subheader("Search Momentum Comparison")

momentum_fig = go.Figure()

momentum_fig.add_trace(
    go.Bar(
        x=summary_df["Company"],
        y=summary_df["Search Momentum %"],
        text=summary_df["Search Momentum %"],
        textposition="auto"
    )
)

momentum_fig.update_layout(
    template="plotly_dark",
    height=500,
    yaxis_title="Search Momentum %"
)

st.plotly_chart(
    momentum_fig,
    use_container_width=True
)

st.subheader("Geographic Search Exposure")

selected_company = st.selectbox(
    "Select company for geographic exposure",
    companies
)

try:
    geo_df = pytrends.interest_by_region(
        resolution="COUNTRY",
        inc_low_vol=True,
        inc_geo_code=False
    )

except Exception as e:
    st.error(f"Geographic search exposure could not be loaded: {e}")
    st.stop()

if geo_df.empty or selected_company not in geo_df.columns:
    st.info("No geographic search exposure data available.")
else:
    country_exposure = (
        geo_df[[selected_company]]
        .reset_index()
        .rename(
            columns={
                "geoName": "Country",
                selected_company: "Search Interest"
            }
        )
    )

    country_exposure = country_exposure.sort_values(
        by="Search Interest",
        ascending=False
    ).head(20)

    st.dataframe(
        country_exposure,
        use_container_width=True
    )

    geo_fig = go.Figure()

    geo_fig.add_trace(
        go.Bar(
            x=country_exposure["Country"],
            y=country_exposure["Search Interest"],
            text=country_exposure["Search Interest"],
            textposition="auto"
        )
    )

    geo_fig.update_layout(
        title=f"Top Countries Searching for {selected_company}",
        template="plotly_dark",
        height=600,
        xaxis_title="Country",
        yaxis_title="Search Interest"
    )

    st.plotly_chart(
        geo_fig,
        use_container_width=True
    )

st.subheader("Executive Search Intelligence Insights")

for _, row in ranking_df.iterrows():

    company = row["Company"]
    sri = row["Search Risk Index"]
    volatility = row["Search Volatility"]
    momentum = row["Search Momentum %"]

    if sri >= 70:
        st.error(
            f"{company} shows very high search risk exposure, "
            f"with strong public attention and unstable search behavior."
        )

    elif sri >= 40:
        st.warning(
            f"{company} shows moderate search risk exposure. "
            f"Search attention is active and should be monitored."
        )

    else:
        st.success(
            f"{company} shows relatively low search risk exposure "
            f"during the selected period."
        )

    st.info(
        f"{company}: Search volatility = {volatility}, "
        f"Search momentum = {momentum}%."
    )
