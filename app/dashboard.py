import streamlit as st
from patient_experience import run as run_patient_experience
from app.discharge_planner import run as run_discharge_planner
from app.capacity_manager import run as run_capacity_manager
from app.strategy_assistant import run as run_strategy_assistant
from app.task_tracker import run as run_task_tracker

def run():
    st.set_page_config(page_title="Healthcare Operations AI Command Center", layout="wide")
    st.title("🏥 Healthcare Operations AI Command Center")

    tabs = st.tabs([
        "Dashboard Overview",
        "Patient Experience",
        "Discharge Planner",
        "Capacity Manager",
        "Strategy Assistant",
        "Task Tracker"
    ])

    with tabs[0]:
        st.subheader("📊 Dashboard Overview")
        st.markdown("""
        This command center provides AI-powered tools to enhance healthcare operational workflows:

        - Deep Patient Feedback Analysis  
        - Smart Discharge Planning  
        - Capacity Forecasting and Utilization  
        - Strategic Decision Assistance  
        - Actionable Task Tracking
        """)

    with tabs[1]:
        run_patient_experience()

    with tabs[2]:
        run_discharge_planner()

    with tabs[3]:
        run_capacity_manager()

    with tabs[4]:
        run_strategy_assistant()

    with tabs[5]:
        run_task_tracker()

if __name__ == "__main__":
    run()