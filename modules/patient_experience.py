import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from transformers import pipeline
import os
import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.cluster import KMeans
import numpy as np
from sklearn.manifold import TSNE
import spacy
from fpdf import FPDF

nltk.download('stopwords')
nlp = spacy.load("en_core_web_sm")

@st.cache_resource
def load_sentiment_model():
    return pipeline("sentiment-analysis")

def detect_text_column(df):
    candidates = []
    for col in df.columns:
        if df[col].dtype == object:
            sample = df[col].dropna().astype(str).str.len().mean()
            if sample > 20:
                candidates.append((col, sample))
    if not candidates:
        return None
    return max(candidates, key=lambda x: x[1])[0]

def clean_text(text):
    text = re.sub(r'[^a-zA-Z ]', '', text)
    text = text.lower()
    tokens = text.split()
    tokens = [w for w in tokens if w not in stopwords.words('english')]
    return ' '.join(tokens)

def extract_keywords(text_series):
    vectorizer = TfidfVectorizer(max_features=100)
    X = vectorizer.fit_transform(text_series)
    features = vectorizer.get_feature_names_out()
    sums = X.sum(axis=0)
    keywords = [(features[i], sums[0, i]) for i in range(len(features))]
    return sorted(keywords, key=lambda x: x[1], reverse=True)[:15]

def summarize_feedback(text_series):
    return text_series.apply(lambda x: ' '.join(x.split()[:25]) + '...')

def topic_modeling(text_series):
    vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
    doc_term_matrix = vectorizer.fit_transform(text_series)
    lda = LatentDirichletAllocation(n_components=5, random_state=42)
    lda.fit(doc_term_matrix)
    topics = []
    for topic in lda.components_:
        words = [vectorizer.get_feature_names_out()[i] for i in topic.argsort()[:-6:-1]]
        topics.append(" ".join(words))
    return topics

def named_entities(text):
    doc = nlp(text)
    return ", ".join([ent.text for ent in doc.ents])

def cluster_feedback(text_series):
    vectorizer = TfidfVectorizer(max_features=100)
    X = vectorizer.fit_transform(text_series)
    kmeans = KMeans(n_clusters=4, random_state=42)
    labels = kmeans.fit_predict(X)
    return labels

def generate_summary_pdf(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Healthcare Feedback Summary Report", ln=True, align='C')
    sentiment_counts = df["Sentiment"].value_counts()
    for idx, val in sentiment_counts.items():
        pdf.cell(200, 10, txt=f"{idx}: {val}", ln=True)
    pdf.output("summary_report.pdf")
    return "summary_report.pdf"

def run():
    st.header("🧠 Patient Experience - Deep Analysis")

    uploaded_file = st.file_uploader("Upload feedback file (CSV or Excel)", type=["csv", "xlsx"])

    if uploaded_file is not None:
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext == ".csv":
            df = pd.read_csv(uploaded_file)
        elif ext == ".xlsx":
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file format. Please upload CSV or Excel.")
            return

        text_col = detect_text_column(df)
        if not text_col:
            st.error("No suitable text column found. Please upload a file with free-text feedback.")
            return

        st.success(f"Detected feedback column: {text_col}")

        df[text_col] = df[text_col].astype(str)
        df["Cleaned"] = df[text_col].apply(clean_text)

        sentiment_model = load_sentiment_model()
        df["Sentiment"] = df["Cleaned"].apply(lambda x: sentiment_model(x)[0]['label'])
        df["Score"] = df["Cleaned"].apply(lambda x: sentiment_model(x)[0]['score'])

        df["Summary"] = summarize_feedback(df["Cleaned"])
        df["Entities"] = df[text_col].apply(named_entities)
        df["Cluster"] = cluster_feedback(df["Cleaned"])

        st.subheader("📋 Feedback Preview with Summary")
        st.dataframe(df[[text_col, "Summary", "Sentiment", "Score", "Entities", "Cluster"]])

        st.subheader("📊 Sentiment Breakdown")
        fig, ax = plt.subplots()
        sns.countplot(data=df, x="Sentiment", palette="Set2", ax=ax)
        st.pyplot(fig)

        st.subheader("🔑 Keyword Extraction")
        keywords = extract_keywords(df["Cleaned"])
        keywords_df = pd.DataFrame(keywords, columns=["Keyword", "Score"])
        st.dataframe(keywords_df)

        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(df["Cleaned"]))
        st.image(wordcloud.to_array(), caption='Feedback WordCloud', use_column_width=True)

        st.subheader("📚 Topic Modeling")
        topics = topic_modeling(df["Cleaned"])
        for i, topic in enumerate(topics):
            st.markdown(f"**Topic {i+1}:** {topic}")

        st.subheader("📁 Download Options")
        st.download_button("Download Analyzed Data", df.to_csv(index=False), file_name="analyzed_feedback.csv", mime="text/csv")

        pdf_path = generate_summary_pdf(df)
        with open(pdf_path, "rb") as f:
            st.download_button("Download Executive Summary PDF", f, file_name="summary_report.pdf", mime="application/pdf")
