import streamlit as st
from database.db_connect import view_clients
from database.workout_manage import add_or_update_workout, view_workout
import random

st.set_page_config(layout="wide")

# Sidebar for Insights
with st.sidebar:
    st.markdown("<h2 style='text-align:center; color:#FF4B4B;'>💡 Workout Insights 💡</h2>", unsafe_allow_html=True)
    st.markdown("---")
    insights = [
        "Did you know that varying your exercises can lead to better muscle engagement?",
        "Remember to incorporate rest days for optimal muscle recovery and growth.",
        "Focus on progressive overload – gradually increasing the intensity or volume of your workouts over time.",
        "Proper form is crucial to prevent injuries and maximize the effectiveness of each exercise.",
        "Staying hydrated plays a significant role in energy levels and overall workout performance.",
        "Consider tracking your progress (e.g., weight lifted, reps) to stay motivated and see improvements.",
        "Nutrition is just as important as your workouts for achieving your fitness goals.",
        "Listen to your body and don't hesitate to adjust your workout plan if needed.",
        "Short bursts of high-intensity interval training (HIIT) can be very effective for calorie burning.",
        "Don't underestimate the benefits of compound exercises that work multiple muscle groups simultaneously.",
    ]
    st.info(random.choice(insights))
    st.markdown("---")
    st.markdown("<p style='text-align:center;'>Your Daily Dose of Fitness Wisdom!</p>", unsafe_allow_html=True)

content_area = st.container()
with content_area:
    st.markdown("<h2 style='text-align:center; color:#FF4B4B;'>🏋️ Workout Plan Management 🏋️</h2>", unsafe_allow_html=True)

    # Check Login
    if not st.session_state.get('logged_in'):
        st.error("🚫 Access Denied! Please Login to Manage Workout Plans.")
        st.stop()

    st.info("Create Customized Workout Plans for Your Clients! 💪")

    # Motivational Banner
    st.markdown(
        """
        <div style='background-color:#1E1E1E; padding:15px; border-radius:10px; color:white;'>
        <b>🔥 Tip:</b> Consistency is More Important than Intensity!
        </div>
        """,
        unsafe_allow_html=True
    )

    clients = view_clients(st.session_state['trainer_name'])

    if not clients:
        st.warning("No Clients Found! Please Add Clients First.")
        st.stop()

    client_dict = {f"{c[1]} (ID: {c[0]})": c[0] for c in clients}

    selected_client = st.selectbox("Select Client", list(client_dict.keys()))
    client_id = client_dict[selected_client]

    existing_workout = view_workout(client_id)

    st.text_area("Current Workout Plan", value=existing_workout if existing_workout else "No Workout Plan Found!", height=200, disabled=True)

    st.markdown("---")

    # Predefined Plans
    st.markdown("### Or Select a Predefined Plan:")

    predefined_plans = {
        "Full Body Beginner": "Day 1: Pushups, Squats\nDay 2: Rest\nDay 3: Lunges, Planks\nDay 4: Rest",
        "Weight Loss": "HIIT, Cardio 30min, Abs Workout",
        "Muscle Gain": "Chest Press, Deadlift, Squats, Shoulder Press",
    }

    selected_plan = st.selectbox("Choose Predefined Plan", list(predefined_plans.keys()))
    selected_plan_data = predefined_plans[selected_plan]

    new_workout = st.text_area("Enter / Update Workout Plan", value=selected_plan_data, height=200)

    if st.button("💾 Save Workout Plan"):
        add_or_update_workout(client_id, new_workout)
        st.success("Workout Plan Saved Successfully! ✅")

    st.markdown("<hr><p style='text-align:center;'>💪 Stay Strong. Train Hard. Win Easy.</p>", unsafe_allow_html=True)