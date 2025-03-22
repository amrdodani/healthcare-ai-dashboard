import streamlit as st
import json
import os

TASK_FILE = "task_list.json"

def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def run():
    st.subheader("AI Task Tracker")
    
    tasks = load_tasks()

    with st.form("add_task"):
        st.markdown("### Add a new task")
        title = st.text_input("Task Title")
        owner = st.text_input("Owner")
        deadline = st.date_input("Deadline")
        status = st.selectbox("Status", ["To Do", "In Progress", "Done"])
        submitted = st.form_submit_button("Add Task")
        if submitted and title:
            tasks.append({
                "title": title,
                "owner": owner,
                "deadline": str(deadline),
                "status": status
            })
            save_tasks(tasks)
            st.success("✅ Task added successfully.")

    st.markdown("### Task List")
    if tasks:
        for i, task in enumerate(tasks):
            st.write(f"**{i+1}. {task['title']}**")
            st.markdown(f"- Owner: {task['owner']}  \n- Deadline: {task['deadline']}  \n- Status: {task['status']}")
    else:
        st.info("No tasks added yet.")
