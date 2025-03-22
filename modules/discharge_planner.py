
import streamlit as st
import pandas as pd
from openai import OpenAI

def run():
    st.subheader("Discharge Planner Assistant")

    uploaded_file = st.file_uploader("Upload data file", type=["csv"], key="discharge_upload")
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("Preview:")
        st.dataframe(df.head())

        if st.button("Analyze with GPT"):
            text_input = "\n".join(df.iloc[:, 0].astype(str).tolist())

            dev_mode = st.secrets.get("DEV_MODE", False)

            if dev_mode:
                st.info("🧪 Running in DEV MODE (no real API call)")
                st.markdown("""
### GPT Analysis (Mocked)
**Issues:**
- Discharge instructions unclear
- Follow-up appointments not scheduled

**Suggestions:**
- Standardize discharge forms
- Automate post-discharge reminders""")
            else:
                try:
                    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": text_input}]
                    )
                    answer = response.choices[0].message.content
                    st.success("✅ GPT Analysis Complete")
                    st.markdown(answer)
                except Exception as e:
                    st.error(f"Error from OpenAI: {e}")
