import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.memory_manager import load_memory
import streamlit as st
import pandas as pd
from utils.memory_manager import load_memory
from modules import patient_experience, discharge_planner, capacity_manager, strategy_planner
import task_tracker

st.set_page_config(page_title="Healthcare GPT Dashboard", layout="wide")
st.title("Healthcare Operations AI Command Center")

tabs = st.tabs([
    "Dashboard Overview", 
    "Patient Experience", 
    "Discharge Planner", 
    "Capacity Manager", 
    "Strategy Assistant", 
    "Task Tracker"
])

with tabs[0]:
    st.subheader("KPI Snapshot")
    uploaded_kpi = st.file_uploader("Upload KPI Dataset (CSV) for Snapshot", type=["csv"])
    if uploaded_kpi:
        df = pd.read_csv(uploaded_kpi)
        st.dataframe(df)
        try:
            cols = st.columns(len(df))
            for i, row in df.iterrows():
                with cols[i % len(cols)]:
                    st.metric(label=row['KPI'], value=str(row['Value']), delta=f"Target: {row['Target']}")
        except Exception as e:
            st.warning(f"KPI format issue: {e}")

    st.subheader("Recent GPT Insights")
    history = load_memory()
    if history:
        for h in history[-3:][::-1]:
            with st.expander(f"Module: {h['module']}"):
                st.markdown(f"**Prompt:** {h['prompt'][:200]}...")
                st.markdown(f"**GPT Response:** {h['response'][:600]}...")
                if st.button(f"Add to Task Tracker ({h['module']})", key=h['prompt'][:30]):
                    st.session_state.task_prefill = h['response']

with tabs[1]: patient_experience.run()
with tabs[2]: discharge_planner.run()
with tabs[3]: capacity_manager.run()
with tabs[4]: strategy_planner.run()
with tabs[5]:
    if "task_prefill" in st.session_state:
        st.markdown("**Auto-filled from GPT Output:**")
        st.write(st.session_state.task_prefill)
    task_tracker.run()
