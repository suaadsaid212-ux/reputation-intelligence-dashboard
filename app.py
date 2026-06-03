import streamlit as st

st.set_page_config(
    page_title="Reputation Intelligence Platform",
    page_icon="🌍",
    layout="wide"
)

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

.hero {
    background: linear-gradient(
        135deg,
        #0f172a,
        #1e293b,
        #0f172a
    );
    padding: 60px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0px 0px 30px rgba(0,255,255,0.15);
}

.big-title {
    font-size: 55px;
    font-weight: 800;
    color: white;
}

.subtitle {
    font-size: 22px;
    color: #cbd5e1;
}

.metric-card {
    background: #111827;
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    border: 1px solid #334155;
}

.metric-value {
    font-size: 42px;
    font-weight: bold;
    color: #22c55e;
}

.metric-label {
    color: white;
    font-size: 16px;
}

.section-box {
    background: #111827;
    padding: 25px;
    border-radius: 15px;
    margin-top: 20px;
    border: 1px solid #334155;
}

.small-title {
    color: white;
    font-size: 24px;
    font-weight: bold;
}

.white-text {
    color: #d1d5db;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# HERO SECTION
# ==================================================

st.markdown("""
<div class="hero">

<div class="big-title">
🌍 Reputation Intelligence Platform
</div>

<br>

<div class="subtitle">
Managing Reputational Risks in the Era of Digital Information
</div>

<br>

Exposure • Vulnerability • Resilience

</div>
""", unsafe_allow_html=True)

st.write("")

# ==================================================
# KPI SECTION
# ==================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
    <div class="metric-value">10,000+</div>
    <div class="metric-label">Organizations</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
    <div class="metric-value">195</div>
    <div class="metric-label">Countries</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
    <div class="metric-value">3</div>
    <div class="metric-label">Core Dimensions</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
    <div class="metric-value">7+</div>
    <div class="metric-label">Intelligence Engines</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ==================================================
# WHAT IS REPUTATION INTELLIGENCE
# ==================================================

with st.expander(
    "📖 What is Reputation Intelligence?"
):

    st.markdown("""

### Reputation Intelligence

Reputation Intelligence is the systematic collection,
analysis and interpretation of information that influences
how stakeholders perceive an organization.

Unlike traditional reputation monitoring, Reputation
Intelligence combines multiple intelligence layers:

• News Intelligence

• Search Intelligence

• Sentiment Analysis

• Financial Intelligence

• Geographic Exposure

• Narrative Intelligence

The goal is to detect reputation threats before they
escalate into organizational crises.

""")

# ==================================================
# FRAMEWORK
# ==================================================

st.markdown("""
<div class="section-box">

<div class="small-title">
Core Reputation Intelligence Framework
</div>

<br>

<h3 style="color:#38bdf8;">Exposure</h3>

<div class="white-text">
Measures visibility and public attention.
</div>

<ul style="color:white;">
<li>News Volume</li>
<li>Search Interest</li>
<li>Geographic Reach</li>
<li>Media Coverage</li>
</ul>

<hr>

<h3 style="color:#f97316;">Vulnerability</h3>

<div class="white-text">
Measures susceptibility to reputation damage.
</div>

<ul style="color:white;">
<li>Negative Sentiment</li>
<li>Narrative Volatility</li>
<li>Subjectivity</li>
<li>Financial Volatility</li>
</ul>

<hr>

<h3 style="color:#22c55e;">Resilience</h3>

<div class="white-text">
Measures the ability to recover from reputation shocks.
</div>

<ul style="color:white;">
<li>Positive Narratives</li>
<li>Trust Signals</li>
<li>Stability Score</li>
<li>Recovery Trends</li>
</ul>

</div>
""", unsafe_allow_html=True)

# ==================================================
# PLATFORM INDICES
# ==================================================

st.subheader("📊 Platform Intelligence Indices")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
    ### NRRI
    
    Narrative Reputation Risk Index
    
    Measures narrative pressure and
    negative information exposure.
    """)

with col2:
    st.success("""
    ### RII
    
    Reputation Intelligence Index
    
    Exposure +
    Vulnerability -
    Resilience
    """)

with col3:
    st.warning("""
    ### Lifecycle Intelligence
    
    Startup
    
    Growth
    
    Maturity
    
    Decline
    
    Recovery
    
    Crisis
    """)

# ==================================================
# DATA SOURCES
# ==================================================

st.subheader("🌐 Data Sources")

st.markdown("""

Current Platform Sources:

✅ Yahoo Finance

✅ Google News

✅ Google Trends

✅ VADER Sentiment

✅ TextBlob Subjectivity

Future Sources:

🔹 LinkedIn Intelligence

🔹 ESG Data

🔹 Sustainability Reports

🔹 Regulatory Data

🔹 Social Media Monitoring

""")

# ==================================================
# DISSERTATION
# ==================================================

st.subheader("🎓 Research Foundation")

st.markdown("""

This platform was developed as part of doctoral research
investigating:

**Managing Reputational Risks of Ethical Disinformation
in the Era of Digital Marketing**

The framework examines:

• Digital Narratives

• Algorithmic Visibility

• Sentiment Volatility

• Disinformation Risk

• Organizational Trust

• Reputation Resilience

""")

# ==================================================
# START BUTTON
# ==================================================

st.success(
    "Use the left sidebar to access all intelligence modules."
)

st.button(
    "🚀 Enter Reputation Intelligence Platform"
)
