
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from transformers import pipeline

# Load sentiment analysis pipeline (no key needed)
@st.cache_resource
def load_sentiment_model():
    return pipeline("sentiment-analysis")

def categorize_feedback(feedback):
    feedback_lower = feedback.lower()
    if "wait" in feedback_lower:
        return "Waiting Time"
    elif "staff" in feedback_lower or "nurse" in feedback_lower:
        return "Staff Behavior"
    elif "doctor" in feedback_lower:
        return "Doctor Communication"
    elif "facility" in feedback_lower or "clean" in feedback_lower:
        return "Facilities"
    elif "bill" in feedback_lower:
        return "Billing"
    elif "appoint" in feedback_lower:
        return "Appointment System"
    else:
        return "Other"

def run():
    st.title("🧠 Patient Experience - Deep Analysis")
    uploaded_file = st.file_uploader("Upload patient feedback CSV", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df.columns = [col.strip() for col in df.columns]
        if "Feedback" not in df.columns:
            st.error("CSV must contain a column named 'Feedback'")
            return

        st.subheader("📄 Raw Feedback Preview")
        st.dataframe(df.head())

        # Step 1: Categorize
        df["Category"] = df["Feedback"].apply(categorize_feedback)

        # Step 2: Sentiment Analysis
        st.info("Running sentiment analysis... Please wait.")
        sentiment_model = load_sentiment_model()
        sentiments = sentiment_model(df["Feedback"].tolist(), truncation=True)
        df["Sentiment"] = [s["label"] for s in sentiments]
        df["Score"] = [round(s["score"], 2) for s in sentiments]

        st.subheader("📊 Categorized Feedback with Sentiment")
        st.dataframe(df)

        # Step 3: Charting
        st.subheader("📈 Feedback Category Distribution")
        fig1, ax1 = plt.subplots()
        df["Category"].value_counts().plot(kind="bar", ax=ax1)
        ax1.set_ylabel("Number of Comments")
        ax1.set_xlabel("Category")
        st.pyplot(fig1)

        st.subheader("😊 Sentiment Breakdown")
        fig2, ax2 = plt.subplots()
        df["Sentiment"].value_counts().plot(kind="pie", autopct="%1.0f%%", ax=ax2)
        ax2.set_ylabel("")
        st.pyplot(fig2)

        st.subheader("📊 Category vs Sentiment")
        fig3, ax3 = plt.subplots(figsize=(8, 4))
        sns.countplot(data=df, x="Category", hue="Sentiment", ax=ax3)
        plt.xticks(rotation=45)
        st.pyplot(fig3)

        # Summary Table
        st.subheader("📋 Summary Table")
        summary = df.groupby(["Category", "Sentiment"]).size().unstack(fill_value=0)
        st.dataframe(summary)
