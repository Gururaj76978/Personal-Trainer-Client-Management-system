import streamlit as st
from database.db_connect import view_clients,get_client_by_id
from database.diet_plan import add_or_update_diet, view_diet_for_client
import plotly.graph_objects as go


def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    return round(weight / (height_m ** 2), 2)

def calculate_maintenance_calories(weight, height_cm, age, gender, activity_level=1.2):
    # Simple Mifflin-St Jeor Equation
    if gender == "Male":
        bmr = 10 * weight + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height_cm - 5 * age - 161
    return int(bmr * activity_level)

if st.session_state.get('logged_in', False):
    st.sidebar.title("🍎 Diet Plan Management")

    menu = st.sidebar.radio("Choose Action", ["Add / Update Diet Plan 📝", "View Diet Plan 📖","Calorie Tracker 📊"])

    st.title("🍽️ Manage Client's Diet Plans")

    trainer_name = st.session_state['trainer_name']

    # Fetch Clients
    clients = view_clients(trainer_name)

    if not clients:
        st.warning("⚠️ No Clients Found. Please add clients first from Client Management.")
    else:
        client_dict = {f"{c[1]} (ID: {c[0]})": c[1] for c in clients}

        if menu == "Add / Update Diet Plan 📝":
            st.title("🥗 Add or Update Diet Plan")
            st.markdown("Select a client, add their meals, and set total daily calories. 🍽️")

            st.markdown("---")

            selected_client = st.selectbox("👤 Select Client", list(client_dict.keys()))

            if selected_client:
                client_name = client_dict[selected_client]

                st.markdown(f"### 📝 Meal Plan for **{client_name}**")

                # Meals Form
                with st.form(key="meal_form"):
                    meal_time = st.selectbox("⏰ Meal Time", ["Breakfast", "Lunch", "Snacks", "Dinner"])
                    food_items = st.text_area("🍎 Food Items (comma separated)", placeholder="e.g., Oats, Banana, Almonds")

                    st.markdown("---")
                    meal_submitted = st.form_submit_button("✅ Save Meal")

                    if meal_submitted:
                        add_or_update_diet(client_name, meal_time, food_items)
                        st.success(f"✅ {meal_time} saved successfully for **{client_name}**!")

                st.markdown("----")

                # ➡️ Now beautifully styled Total Calories Box
                st.markdown("### 🔥 Set Daily Calories Target")

                with st.container():
                    st.markdown(
                        """
                        <div style='background-color: #f9f9f9; padding: 20px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);'>
                            <h4 style='color: #ff4b4b;'>🔥 Total Daily Calories</h4>
                            <p style='color: gray;'>Enter the target calories for the whole day</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                total_calories = st.number_input("Enter Total Calories (kcal)", min_value=0, step=10, help="Enter total daily calories target")

                if st.button("💾 Save Total Calories"):
                    add_or_update_diet(client_name, "TotalCalories", str(total_calories))
                    st.success(f"✅ Total Calories of **{total_calories} kcal** saved for **{client_name}**!")

            st.markdown("---")
            st.info("💡 Tip: Add each meal separately, then set total daily calories target for client goals.")


        elif menu == "View Diet Plan 📖":
            st.subheader("📋 View Client's Diet Plan")

            with st.container():
                selected_client = st.selectbox("👤 Select Client to View Plan", list(client_dict.keys()))

                if selected_client:
                    client_name = client_dict[selected_client]
                    diet_data = view_diet_for_client(client_name)

                    if diet_data:
                        st.success(f"Showing diet plan for **{client_name}** 👇")

                        total_calories = diet_data.get("TotalCalories", "Not Specified")

                        # Display total calories on top
                        st.markdown(f"### 🔥 Total Calories: **{total_calories} kcal**")
                        st.markdown("---")

                        for meal, food in diet_data.items():
                            if meal != "TotalCalories":
                                # Split food text into meal items and calories if you want
                                st.markdown(f"""
                                <div style='
                                    background-color:#2C2F33;
                                    padding: 15px;
                                    border-radius: 10px;
                                    margin-bottom: 10px;
                                    box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
                                '>
                                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                                        <h4 style='margin: 0;'>🍽️ {meal}</h4>
                                    </div>
                                    <p style='margin-top: 10px; font-size: 16px;'>{food}</p>
                                </div>
                                """, unsafe_allow_html=True)
                    else:
                        st.warning("🚫 No Diet Plan Found for this Client")


        elif menu == "Calorie Tracker 📊":
            st.title("📊 Calorie & BMI Tracker")

            selected_client = st.selectbox("👤 Select Client", list(client_dict.keys()))

            if selected_client:
                client_name = client_dict[selected_client]
                client_id = int(selected_client.split("ID: ")[1].rstrip(")"))
                client_data = get_client_by_id(client_id)

                if client_data:
                    _, name, age, gender, height_cm, weight = client_data[:6]

                    # Calculations
                    bmi = calculate_bmi(weight, height_cm)
                    maintenance_cal = calculate_maintenance_calories(weight, height_cm, age, gender)
                    diet_data = view_diet_for_client(client_name)
                    current_cal = int(diet_data.get("TotalCalories", 0))

                    # ➡️ Client Basic Info Card
                    st.markdown("---")
                    st.subheader(f"🧍 Client: {client_name}")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f"📏 **Height:** {height_cm} cm")
                        st.markdown(f"🎂 **Age:** {age}")
                    with col2:
                        st.markdown(f"⚖️ **Weight:** {weight} kg")
                        st.markdown(f"🧬 **Gender:** {gender}")
                    with col3:
                        st.markdown(f"🔢 **BMI:** {bmi}")

                    st.markdown("---")

                    # ➡️ Calories Card
                    st.subheader("🍽️ Calorie Summary")
                    
                    cal1, cal2 = st.columns(2)
                    with cal1:
                        st.markdown(f"<h3 style='color: teal;'>🔥 Maintenance (TDEE): {maintenance_cal} kcal</h3>", unsafe_allow_html=True)
                    with cal2:
                        st.markdown(f"<h3 style='color: orange;'>🍴 Current Diet: {current_cal} kcal</h3>", unsafe_allow_html=True)

                    st.markdown("---")

                    # ➡️ Gauge Meter
                    st.subheader("📊 Calorie Deficit / Surplus Status")

                    fig = go.Figure(go.Indicator(
                        mode="gauge+number+delta",
                        value=current_cal,
                        delta={'reference': maintenance_cal, 'increasing': {'color': "red"}, 'decreasing': {'color': "green"}},
                        gauge={
                            'axis': {'range': [0, maintenance_cal + 1000]},
                            'bar': {'color': "darkblue"},
                            'steps': [
                                {'range': [0, maintenance_cal], 'color': "lightgreen"},
                                {'range': [maintenance_cal, maintenance_cal + 1000], 'color': "lightcoral"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': maintenance_cal}
                        }
                    ))
                    st.plotly_chart(fig, use_container_width=True)

                    st.markdown("---")

                    # ➡️ Insight Text
                    st.subheader("📈 Insight")

                    if current_cal < maintenance_cal:
                        st.success(f"✅ You are in a calorie deficit of **{maintenance_cal - current_cal} kcal**. Good for fat loss! 💪")
                    elif current_cal > maintenance_cal:
                        st.warning(f"⚠️ You are in a calorie surplus of **{current_cal - maintenance_cal} kcal**. Useful for muscle gain! 🏋️")
                    else:
                        st.info("🎯 You are exactly at maintenance calories. Great for weight maintenance!")

                    st.markdown("---")


    st.sidebar.markdown("---")
    st.sidebar.success(f"Logged in as: **{trainer_name}**")
    st.sidebar.button('Logout', on_click=lambda: st.session_state.update(logged_in=False, trainer_name=None))

else:
    st.markdown("""
        <div style='text-align: center; padding: 30px; background-color: #2c2c2c; border-radius: 10px;'>
            <h2 style='color: #FF4B4B;'>⚠️ Access Denied</h2>
            <p style='color: #DDDDDD; font-size: 20px;'>Please <span style='color: #FF4B4B; font-weight: bold;'>Log In</span> to access Diet plan features.</p>
        </div>
    """, unsafe_allow_html=True)
