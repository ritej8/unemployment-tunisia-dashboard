# =========================================
# IMPORTS
# =========================================
import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="Tunisia Unemployment Dashboard",
    layout="wide",
    page_icon="📊"
)

# =========================================
# LOAD DATA
# =========================================
@st.cache_data
def load_data():
    df = pd.read_csv("data/tunisia_unemployment_clean.csv")
    return df

df = load_data()

# =========================================
# DATA CLEANING
# =========================================
df = df.dropna()
df = df.sort_values("year").reset_index(drop=True)

# =========================================
# SIDEBAR
# =========================================
st.sidebar.header("🔎 Filters")

min_year = int(df["year"].min())
max_year = int(df["year"].max())

year_range = st.sidebar.slider(
    "Select Year Range",
    min_year,
    max_year,
    (min_year, max_year)
)

df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]

# =========================================
# HEADER
# =========================================
st.title("📊 Unemployment Analysis in Tunisia")
st.markdown("Interactive dashboard exploring unemployment trends, gender disparities, and youth challenges.")

# =========================================
# KPI SECTION
# =========================================
latest = df.iloc[-1]
first = df.iloc[0]

trend = latest["total_unemployment"] - first["total_unemployment"]

col1, col2, col3, col4 = st.columns(4)

col1.metric("Average Rate", f"{df['total_unemployment'].mean():.2f}%")
col2.metric("Latest Rate", f"{latest['total_unemployment']:.2f}%", f"{trend:.2f}%")
col3.metric("Max Rate", f"{df['total_unemployment'].max():.2f}%")
col4.metric("Youth Max", f"{df['youth_unemployment'].max():.2f}%")

st.markdown("---")

# =========================================
# TREND
# =========================================
st.subheader("📈 Unemployment Trend")

fig1 = px.line(df, x="year", y="total_unemployment", markers=True)
fig1.update_layout(template="plotly_white")

st.plotly_chart(fig1, use_container_width=True)

st.caption("Unemployment shows fluctuations over time with periods of increase linked to economic instability.")

# =========================================
# GENDER
# =========================================
st.subheader("👥 Gender Comparison")

fig2 = px.line(
    df,
    x="year",
    y=["male_unemployment", "female_unemployment"],
    markers=True
)

fig2.update_layout(template="plotly_white")

st.plotly_chart(fig2, use_container_width=True)

st.caption("Differences between male and female unemployment highlight inequalities in the labor market.")

# =========================================
# YOUTH
# =========================================
st.subheader("🎓 Youth Unemployment")

fig3 = px.line(df, x="year", y="youth_unemployment", markers=True)
fig3.update_layout(template="plotly_white")

st.plotly_chart(fig3, use_container_width=True)

st.caption("Youth unemployment remains significantly higher than the overall rate.")

# =========================================
# COMPARISON
# =========================================
st.subheader("⚖️ Youth vs Total")

fig4 = px.line(
    df,
    x="year",
    y=["total_unemployment", "youth_unemployment"],
    markers=True
)

fig4.update_layout(template="plotly_white")

st.plotly_chart(fig4, use_container_width=True)

st.caption("The persistent gap suggests structural employment challenges for young people.")

# =========================================
# ADVANCED METRICS
# =========================================
df["gender_gap"] = df["female_unemployment"] - df["male_unemployment"]
df["youth_ratio"] = df["youth_unemployment"] / df["total_unemployment"]

st.subheader("📊 Advanced Indicators")

col1, col2 = st.columns(2)

with col1:
    fig5 = px.line(df, x="year", y="gender_gap")
    st.plotly_chart(fig5, use_container_width=True)

with col2:
    fig6 = px.line(df, x="year", y="youth_ratio")
    st.plotly_chart(fig6, use_container_width=True)

# =========================================
# INSIGHTS SECTION
# =========================================
st.markdown("---")
st.subheader("🧠 Key Insights")

peak_year = df.loc[df["total_unemployment"].idxmax(), "year"]
peak_value = df["total_unemployment"].max()

avg_gap = df["gender_gap"].mean()
avg_ratio = df["youth_ratio"].mean()

if trend > 0:
    st.markdown(f"📈 Unemployment increased by {trend:.2f}% over the selected period.")
else:
    st.markdown(f"📉 Unemployment decreased by {abs(trend):.2f}% over the selected period.")

st.markdown(f"📊 Peak unemployment was {peak_value:.2f}% in {peak_year}.")

if avg_gap > 0:
    st.markdown("👥 Female unemployment is generally higher than male unemployment.")
else:
    st.markdown("👥 Male unemployment is higher or similar to female unemployment.")

st.markdown(f"🎓 Youth unemployment is on average {avg_ratio:.2f} times higher than total unemployment.")

# =========================================
# FOOTER
# =========================================
st.markdown("---")
st.markdown("📌 Data Source: World Bank | Project by: ritej")