import streamlit as st
from app.dashboard import run as run_dashboard
from modules.patient_experience import run as run_patient_experience
from modules.discharge_planner import run as run_discharge_planner
from modules.capacity_manager import run as run_capacity_manager
from modules.strategy_planner import run as run_strategy_planner
from modules.task_tracker import run as run_task_tracker

st.set_page_config(page_title="Healthcare Operations AI Command Center", layout="wide")

st.title("🏥 Healthcare Operations AI Command Center")

menu = st.sidebar.radio("Navigation", [
    "Dashboard Overview",
    "Patient Experience",
    "Discharge Planner",
    "Capacity Manager",
    "Strategy Assistant",
    "Task Tracker"
])

if menu == "Dashboard Overview":
    run_dashboard()
elif menu == "Patient Experience":
    run_patient_experience()
elif menu == "Discharge Planner":
    run_discharge_planner()
elif menu == "Capacity Manager":
    run_capacity_manager()
elif menu == "Strategy Assistant":
    run_strategy_planner()
elif menu == "Task Tracker":
    run_task_tracker()