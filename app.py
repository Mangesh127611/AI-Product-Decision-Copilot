
import streamlit as st
import pandas as pd

# --------------------------------------------------
# APP CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Product Decision Copilot",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 AI Product Decision Copilot")
st.write(
    "Turn customer feedback into product priorities "
    "and actionable decisions."
)

# --------------------------------------------------
# SAMPLE CUSTOMER FEEDBACK
# --------------------------------------------------

sample_feedback = pd.DataFrame({
    "Feedback": [
        "Signup process is too confusing.",
        "Dashboard takes too long to load.",
        "I cannot find the products I need.",
        "Checkout fails when I try to pay.",
        "Customer support takes too long to respond.",
        "Onboarding should be simpler.",
        "Search filters are not useful.",
        "The app is slow when opening reports.",
        "I do not understand how to use this feature.",
        "Payment failed twice during checkout.",
        "I need better product recommendations.",
        "The dashboard is difficult to understand.",
        "Support should answer faster.",
        "New users need a clearer setup guide.",
        "Product search should be more accurate."
    ]
})


def identify_theme(feedback):
    text = str(feedback).lower()

    keywords = {
        "Onboarding": [
            "onboarding", "signup", "sign up",
            "setup", "new user"
        ],
        "Performance": [
            "slow", "loading", "load time",
            "performance", "lag"
        ],
        "Search & Discovery": [
            "search", "find products", "filters",
            "recommendations", "discovery"
        ],
        "Checkout & Payment": [
            "checkout", "payment", "pay",
            "billing", "transaction"
        ],
        "Customer Support": [
            "support", "response", "respond",
            "help", "answers"
        ],
        "Usability": [
            "confusing", "difficult", "understand",
            "hard to use", "not useful"
        ]
    }

    for theme, words in keywords.items():
        if any(word in text for word in words):
            return theme

    return "Other"


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.header("Project Controls")

uploaded_file = st.sidebar.file_uploader(
    "Upload customer feedback CSV (optional)",
    type=["csv"],
    help="Your CSV must contain a column named Feedback."
)

if uploaded_file is not None:
    try:
        uploaded_df = pd.read_csv(uploaded_file)

        if "Feedback" not in uploaded_df.columns:
            st.sidebar.error(
                "CSV must contain a column named Feedback."
            )
            feedback_df = sample_feedback.copy()
            st.sidebar.info("Using sample feedback instead.")
        else:
            feedback_df = uploaded_df.copy()
            st.sidebar.success("Uploaded feedback loaded.")

    except Exception as error:
        st.sidebar.error(f"Could not read CSV: {error}")
        feedback_df = sample_feedback.copy()
else:
    feedback_df = sample_feedback.copy()
    st.sidebar.info("Using built-in sample feedback.")

feedback_df = feedback_df.dropna(subset=["Feedback"]).copy()
feedback_df["Feedback"] = feedback_df["Feedback"].astype(str)
feedback_df = feedback_df[
    feedback_df["Feedback"].str.strip() != ""
].copy()

feedback_df["Theme"] = feedback_df["Feedback"].apply(
    identify_theme
)

# --------------------------------------------------
# FEATURE PRIORITIZATION
# --------------------------------------------------

st.header("1. Feature Prioritization")

st.write(
    "Adjust the ratings to explore how different product "
    "decisions affect the roadmap."
)

default_features = pd.DataFrame({
    "Feature": [
        "Simplify onboarding",
        "Add advanced filters",
        "Personalized recommendations",
        "Team onboarding guide"
    ],
    "Impact": [5, 3, 5, 4],
    "Confidence": [4, 4, 3, 4],
    "Effort": [2, 3, 5, 2],
    "Strategic Fit": [5, 3, 4, 4]
})

edited_features = st.data_editor(
    default_features,
    use_container_width=True,
    hide_index=True,
    key="feature_editor",
    column_config={
        "Feature": st.column_config.TextColumn(
            "Feature",
            disabled=True
        ),
        "Impact": st.column_config.NumberColumn(
            "Impact (1–5)",
            min_value=1,
            max_value=5,
            step=1
        ),
        "Confidence": st.column_config.NumberColumn(
            "Confidence (1–5)",
            min_value=1,
            max_value=5,
            step=1
        ),
        "Effort": st.column_config.NumberColumn(
            "Effort (1–5)",
            min_value=1,
            max_value=5,
            step=1
        ),
        "Strategic Fit": st.column_config.NumberColumn(
            "Strategic Fit (1–5)",
            min_value=1,
            max_value=5,
            step=1
        )
    }
)

features = edited_features.copy()

features["Priority Score"] = (
    features["Impact"]
    * features["Confidence"]
    * features["Strategic Fit"]
    / features["Effort"]
).round(2)

features = features.sort_values(
    "Priority Score",
    ascending=False
).reset_index(drop=True)

st.subheader("Ranked Product Roadmap")

st.dataframe(
    features,
    use_container_width=True,
    hide_index=True
)

st.bar_chart(
    features.set_index("Feature")["Priority Score"]
)

st.download_button(
    "Download Feature Roadmap",
    data=features.to_csv(index=False).encode("utf-8"),
    file_name="feature_roadmap.csv",
    mime="text/csv"
)

st.caption(
    "Priority score = Impact × Confidence × Strategic Fit ÷ Effort. "
    "Higher scores indicate stronger relative priority under this "
    "scoring model."
)

# --------------------------------------------------
# CUSTOMER FEEDBACK AND OPPORTUNITY SCORING
# --------------------------------------------------

st.divider()
st.header("2. Customer Feedback Analysis")

if feedback_df.empty:
    st.warning("No feedback comments are available.")
    st.stop()

theme_counts = (
    feedback_df["Theme"]
    .value_counts()
    .rename_axis("Theme")
    .reset_index(name="Comments")
)

st.subheader("Feedback Themes")

st.dataframe(
    theme_counts,
    use_container_width=True,
    hide_index=True
)

st.bar_chart(
    theme_counts.set_index("Theme")["Comments"]
)

selected_theme = st.selectbox(
    "Explore customer comments by theme",
    theme_counts["Theme"].tolist()
)

st.dataframe(
    feedback_df.loc[
        feedback_df["Theme"] == selected_theme,
        ["Feedback", "Theme"]
    ],
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# PRODUCT OPPORTUNITY SCORING
# --------------------------------------------------

st.divider()
st.header("3. Product Opportunity Scoring")

st.write(
    "Rank recurring customer problems using feedback frequency, "
    "estimated impact, confidence, and effort."
)

opportunity_data = {
    "Onboarding": {
        "Problem": "Users struggle to get started",
        "Impact": 5,
        "Confidence": 4,
        "Effort": 2
    },
    "Performance": {
        "Problem": "Pages and dashboards load slowly",
        "Impact": 5,
        "Confidence": 4,
        "Effort": 4
    },
    "Search & Discovery": {
        "Problem": "Users struggle to find products",
        "Impact": 4,
        "Confidence": 4,
        "Effort": 3
    },
    "Checkout & Payment": {
        "Problem": "Customers experience payment friction",
        "Impact": 5,
        "Confidence": 4,
        "Effort": 4
    },
    "Customer Support": {
        "Problem": "Customers wait too long for help",
        "Impact": 3,
        "Confidence": 4,
        "Effort": 2
    },
    "Usability": {
        "Problem": "Product features are confusing",
        "Impact": 4,
        "Confidence": 3,
        "Effort": 3
    },
    "Other": {
        "Problem": "Unclassified customer problems",
        "Impact": 2,
        "Confidence": 2,
        "Effort": 2
    }
}

opportunities = []
total_comments = len(feedback_df)

for theme, details in opportunity_data.items():
    count = int((feedback_df["Theme"] == theme).sum())

    if count == 0:
        continue

    frequency_score = count / total_comments * 5

    score = (
        frequency_score
        * details["Impact"]
        * details["Confidence"]
        / details["Effort"]
    )

    opportunities.append({
        "Theme": theme,
        "Customer Problem": details["Problem"],
        "Comments": count,
        "Frequency Score": round(frequency_score, 2),
        "Impact": details["Impact"],
        "Confidence": details["Confidence"],
        "Effort": details["Effort"],
        "Opportunity Score": round(score, 2)
    })

opportunity_df = pd.DataFrame(opportunities)

opportunity_df = opportunity_df.sort_values(
    "Opportunity Score",
    ascending=False
).reset_index(drop=True)

opportunity_df.insert(
    0,
    "Rank",
    range(1, len(opportunity_df) + 1)
)

st.dataframe(
    opportunity_df,
    use_container_width=True,
    hide_index=True
)

st.bar_chart(
    opportunity_df.set_index("Theme")["Opportunity Score"]
)

st.download_button(
    "Download Opportunity Report",
    data=opportunity_df.to_csv(index=False).encode("utf-8"),
    file_name="product_opportunities.csv",
    mime="text/csv"
)

# --------------------------------------------------
# EXECUTIVE DASHBOARD
# --------------------------------------------------

st.divider()
st.header("4. Executive Dashboard")

st.write(
    "A high-level summary to support product planning and "
    "stakeholder discussions."
)

top_feature = features.iloc[0]
top_opportunity = opportunity_df.iloc[0]
most_common_theme = theme_counts.iloc[0]

metric1, metric2 = st.columns(2)

metric1.metric(
    "Customer Feedback Comments",
    total_comments
)

metric2.metric(
    "Feedback Themes",
    len(theme_counts)
)

metric3, metric4 = st.columns(2)

metric3.metric(
    "Highest-Priority Feature",
    top_feature["Feature"]
)

metric4.metric(
    "Top Customer Problem",
    top_opportunity["Theme"]
)

st.subheader("Recommended Product Focus")

st.success(
    f"**Feature to consider:** {top_feature['Feature']} "
    f"(score: {top_feature['Priority Score']})"
)

st.info(
    f"**Customer problem to investigate:** "
    f"{top_opportunity['Customer Problem']} "
    f"(opportunity score: {top_opportunity['Opportunity Score']})"
)

st.subheader("Suggested Next Steps")

recommendations = {
    "Onboarding": (
        "Review the signup journey and measure onboarding completion."
    ),
    "Performance": (
        "Measure page load times and investigate slow user journeys."
    ),
    "Search & Discovery": (
        "Test search relevance and measure successful product searches."
    ),
    "Checkout & Payment": (
        "Investigate payment failures and measure checkout conversion."
    ),
    "Customer Support": (
        "Review recurring support requests and improve help content."
    ),
    "Usability": (
        "Test confusing workflows and measure task completion."
    ),
    "Other": (
        "Review uncategorized feedback to identify new problems."
    )
}

st.write(
    recommendations.get(
        top_opportunity["Theme"],
        "Review the customer feedback and identify next steps."
    )
)

st.caption(
    "This dashboard uses sample data or uploaded feedback, "
    "keyword-based theme classification, and illustrative scoring "
    "assumptions. It is a decision-support prototype, not a "
    "real AI-generated analysis. Validate conclusions with research."
)

# --------------------------------------------------
# EXPORT EXECUTIVE SUMMARY
# --------------------------------------------------

summary = f"""# AI Product Decision Copilot — Executive Summary

## Feedback
- Total comments: {total_comments}
- Most common feedback theme: {most_common_theme['Theme']}
- Comments in that theme: {most_common_theme['Comments']}

## Feature Prioritization
- Highest-priority feature: {top_feature['Feature']}
- Priority score: {top_feature['Priority Score']}

## Product Opportunity
- Top customer problem: {top_opportunity['Customer Problem']}
- Opportunity theme: {top_opportunity['Theme']}
- Opportunity score: {top_opportunity['Opportunity Score']}

## Suggested Next Step
{recommendations.get(top_opportunity['Theme'], 'Review customer feedback.')}

## Methodology
Feature priority = Impact × Confidence × Strategic Fit ÷ Effort.

Opportunity score = Feedback Frequency Score × Impact × Confidence ÷ Effort.

Scores depend on assumptions and should be validated with customer research.
"""

st.download_button(
    "Download Executive Summary",
    data=summary,
    file_name="executive_summary.md",
    mime="text/markdown"
)

st.divider()

st.caption(
    "AI Product Decision Copilot | Portfolio Project | "
    "Python • Streamlit • Pandas"
)
