import streamlit as st
from data_base import insert_task, get_all_tasks, deactivate_task, init_db
from Gcallender.calender_reminder import shedule_reminders
from datetime import datetime


# Initialize database only once per session
if "db_initialized" not in st.session_state:
    init_db()
    st.session_state["db_initialized"] = True

st.set_page_config(
    layout="wide", 
    page_title="Spaced Repetition System", 
    initial_sidebar_state="collapsed"
)

st.title("🧠 Spaced Repetition Task Manager")

# Interval patterns
interval_options = {
    "Beginner (1, 3, 7, 16, 30 days)": [1, 3, 7, 16, 30],
    "Intermediate (1, 2, 4, 8, 15 days)": [1, 2, 4, 8, 15],
    "Aggressive (1, 2, 3, 5, 7 days)": [1, 2, 3, 5, 7],
    "long_rep (7,16,30)":[7, 16, 30],
    "Custom": None
}

# Add new task section
st.header("➕ Add New Task")

with st.form("add_task_form"):
    task_input = st.text_area(
        "Task Description", 
        placeholder="e.g., Review LeetCode problems 1-5",
        help="Enter a clear description of what you want to be reminded about"
    )
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_pattern = st.selectbox(
            "Choose interval pattern", 
            list(interval_options.keys())
        )
    
    with col2:
        if selected_pattern == "Custom":
            custom_intervals = st.text_input(
                "Custom intervals (comma-separated days)",
                placeholder="1,2,4,7,14"
            )
    
    submitted = st.form_submit_button("Add Task", use_container_width=True)
    
    if submitted:
        if not task_input.strip():
            st.error("Please enter a task description")
        else:
            try:
                # Get intervals
                if selected_pattern == "Custom":
                    if not custom_intervals:
                        st.error("Please enter custom intervals")
                        st.stop()
                    intervals = [int(x.strip()) for x in custom_intervals.split(',')]
                else:
                    intervals = interval_options[selected_pattern]
                
                # Insert task into database
                task_id = insert_task(task_input.strip(), intervals)
                
                # Schedule reminders
                scheduled_times = shedule_reminders(task_input.strip(), intervals)
                
                st.success(f"✅ Task added successfully!")
                st.info(f"📅 Reminders scheduled for: {', '.join(scheduled_times)}")
                
                # Refresh the page to show updated tasks
                              
            except ValueError:
                st.error("Invalid interval format. Use comma-separated numbers (e.g., 1,3,7)")
            except Exception as e:
                st.error(f"Error adding task: {e}")

# Display current tasks
st.header("📋 Current Tasks")

tasks = get_all_tasks()

if tasks:
    for task_id, details in tasks.items():
        with st.container():
            st.divider()
            
            col1, col2, col3 = st.columns([4, 2, 1])
            
            with col1:
                st.markdown(f"**{details['task_name']}**")
                created_date = datetime.fromisoformat(details['date_created']).strftime("%Y-%m-%d %H:%M")
                st.caption(f"Created: {created_date}")
            
            with col2:
                if details['intervals']:
                    interval_text = ", ".join(map(str, sorted(details['intervals'])))
                    st.markdown(f"📅 **Intervals:** {interval_text} days")
                else:
                    st.markdown("📅 **No intervals set**")
            
            with col3:
                if st.button("🗑️", key=f"delete_{task_id}", help="Delete task"):
                    deactivate_task(task_id)
                    st.success(f"Task deleted!")
                    st.rerun()
else:
    st.info("No tasks yet. Add one above! ⬆️")

# Statistics
st.header("📊 Statistics")
if tasks:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Active Tasks", len(tasks))
    
    with col2:
        total_reminders = sum(len(task['intervals']) for task in tasks.values())
        st.metric("Total Scheduled Reminders", total_reminders)
    
    with col3:
        avg_intervals = total_reminders / len(tasks) if tasks else 0
        st.metric("Average Intervals per Task", f"{avg_intervals:.1f}")

# Instructions
with st.expander("ℹ️ How it works"):
    st.markdown("""
    **Spaced Repetition System**
    
    This app helps you implement spaced repetition for better learning retention:
    
    1. **Add a task** - Describe what you want to review/practice
    2. **Choose intervals** - Select how often you want reminders:
       - **Beginner**: Longer intervals for gradual reinforcement
       - **Intermediate**: Balanced approach for regular review
       - **Aggressive**: Frequent reminders for intensive learning
       - **Custom**: Set your own interval pattern
    3. **Get reminders** - Receive email notifications at 9:00 AM on scheduled days
    
    The system is based on the proven spaced repetition technique where review intervals increase over time for optimal memory retention.
    """)

