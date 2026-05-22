import streamlit as st
import pandas as pd
import numpy as np
from pytrends.request import TrendReq
# =====================================================
# GOOGLE TRENDS SETUP
# =====================================================

pytrends = TrendReq(hl='en-GB', tz=0)




st.set_page_config(
    page_title="CRM Demand Scanner",
    layout="wide"
)

st.title("CRM Demand Scanner")
st.write(
    "Use this tool to score potential demand for CRM, campaign operations, "
    "contact pressure, and send allocation tools."
)

st.sidebar.header("Keyword Inputs")

default_keywords = """CRM campaign operations
contact pressure
send volume management
campaign governance
audience segmentation
lifecycle marketing
marketing automation
Braze
Salesforce Marketing Cloud
Adobe Campaign
Iterable
customer journey orchestration
campaign operations analyst
CRM operations manager"""

keywords_text = st.sidebar.text_area(
    "Enter one keyword per line",
    value=default_keywords,
    height=300
)

keywords = [
    kw.strip()
    for kw in keywords_text.split("\n")
    if kw.strip()
]

st.sidebar.header("Manual Signal Scores")

job_weight = st.sidebar.slider("Job post signal weight", 1, 10, 5)
search_weight = st.sidebar.slider("Search trend signal weight", 1, 10, 4)
community_weight = st.sidebar.slider("Community pain signal weight", 1, 10, 4)
competitor_weight = st.sidebar.slider("Competitor signal weight", 1, 10, 3)

st.subheader("Demand Research Template")

st.write(
    "For each keyword, add manual scores from 0 to 10. "
    "Later, these can be automated using APIs."
)
def get_google_trend_score(keyword):

    try:

        pytrends.build_payload(
            [keyword],
            timeframe='today 12-m',
            geo='GB'
        )

        trend_data = pytrends.interest_over_time()

        if trend_data.empty:
            return 0

        score = trend_data[keyword].mean()

        return round(score, 2)

    except Exception:
        return 0
# =====================================================
# GOOGLE TRENDS FUNCTION
# =====================================================

def get_google_trend_score(keyword):

    try:

        pytrends.build_payload(
            [keyword],
            timeframe='today 12-m',
            geo='GB'
        )

        trend_data = pytrends.interest_over_time()

        if trend_data.empty:
            return 0

        score = trend_data[keyword].mean()

        return round(score, 2)

    except Exception:
        return 0

edited_df = st.data_editor(
    df,
    use_container_width=True,
    num_rows="dynamic"
)

edited_df["Weighted_Demand_Score"] = (
    edited_df["Job_Post_Score"] * job_weight
    + edited_df["Search_Trend_Score"] * search_weight
    + edited_df["Community_Pain_Score"] * community_weight
    + edited_df["Competitor_Score"] * competitor_weight
)

edited_df["Weighted_Demand_Score"] = edited_df["Weighted_Demand_Score"].round(2)

ranked_df = edited_df.sort_values(
    "Weighted_Demand_Score",
    ascending=False
)

st.subheader("Ranked Demand Signals")
st.dataframe(ranked_df, use_container_width=True)

st.subheader("Top Opportunities")

top_n = st.slider("Number of top opportunities to show", 3, 20, 10)

st.dataframe(
    ranked_df.head(top_n),
    use_container_width=True
)

csv = ranked_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Demand Research CSV",
    data=csv,
    file_name="crm_demand_research.csv",
    mime="text/csv"
)
