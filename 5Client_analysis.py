import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from database.db_connect import get_connection  # Assuming this exists
from database.db_connect import view_clients
st.set_page_config(page_title="Client Progress Analysis", layout="wide")

# Sidebar Design
st.sidebar.title("📊 Analysis Dashboard")
st.sidebar.markdown("### Select Analysis Type")
analysis_type = st.sidebar.radio("Choose Option", ["Weight Progression", "BMI Analysis"])

st.sidebar.markdown("---")
st.sidebar.markdown("Need Help? Contact Support 👇")
st.sidebar.markdown("📞 +91-9876543210")
st.sidebar.markdown("📧 trainerapp@gmail.com")
st.sidebar.markdown("🌐 www.trainerapp.com")

if st.session_state.get('logged_in'):
    # Load Data from JSON
    try:
        with open('client_progress.json', 'r') as file:
            progress_data = json.load(file)
    except FileNotFoundError:
        st.error("Progress Data File Not Found!")
        st.stop()

    clients = view_clients(st.session_state['trainer_name'])
    client_names = [c[1] for c in clients]
    

    if client_names:
        selected_client = st.sidebar.selectbox("Select Client", client_names)
        client_data = progress_data.get(selected_client, [])

        if not client_data:
            st.warning(f"No progress data available for {selected_client}.")
            st.stop()

        df = pd.DataFrame(client_data)

        if df.empty:
            st.warning(f"No progress data found for {selected_client}.")
            st.stop()

        st.title(f"Client Progress Report: {selected_client}")

# Weight Progression Analysis with Multiple Charts
        if analysis_type == "Weight Progression":
            st.subheader("📈 Weight Progression Over Time")

            # Line Chart
            fig_line = px.line(df, x='date', y='weight',
                               title="Line Chart",
                               markers=True,
                               labels={'date': 'Date', 'weight': 'Weight (kg)'})
            fig_line.update_traces(line=dict(color='#66c2a5'))
            fig_line.update_layout(xaxis_title="Date", yaxis_title="Weight (kg)",
                                  xaxis=dict(showgrid=True),
                                  yaxis=dict(showgrid=True),
                                  plot_bgcolor='black')
            st.plotly_chart(fig_line, use_container_width=True)

            st.markdown("---")

            # Bar Chart
            fig_bar = px.bar(df, x='date', y='weight',
                              title="Bar Chart",
                              labels={'date': 'Date', 'weight': 'Weight (kg)'})
            fig_bar.update_traces(marker_color='#8da0cb')
            fig_bar.update_layout(xaxis_title="Date", yaxis_title="Weight (kg)",
                                 xaxis=dict(showgrid=False),
                                 yaxis=dict(showgrid=True),
                                 plot_bgcolor='black')
            st.plotly_chart(fig_bar, use_container_width=True)

            st.markdown("---")

            # Area Chart
            fig_area = px.area(df, x='date', y='weight',
                                title="Area Chart",
                                labels={'date': 'Date', 'weight': 'Weight (kg)'})
            fig_area.update_traces(fillcolor='rgba(171, 130, 191, 0.6)')
            fig_area.update_layout(xaxis_title="Date", yaxis_title="Weight (kg)",
                                   xaxis=dict(showgrid=True),
                                   yaxis=dict(showgrid=True),
                                   plot_bgcolor='black')
            st.plotly_chart(fig_area, use_container_width=True)


        # BMI Chart
        elif analysis_type == "BMI Analysis":
            st.subheader("🧮 BMI Progress Over Time")
            df['bmi'] = df['weight'] / (df['height']/100) ** 2
            fig = px.line(df, x='date', y='bmi', title=f"BMI Trend of {selected_client}", markers=True)
            fig.update_traces(line=dict(color='blue'))
            fig.add_hrect(y0=0, y1=18.5, line_width=0, fillcolor="yellow", opacity=0.2, annotation_text="Underweight")
            fig.add_hrect(y0=18.5, y1=24.9, line_width=0, fillcolor="green", opacity=0.2, annotation_text="Normal")
            fig.add_hrect(y0=25, y1=29.9, line_width=0, fillcolor="orange", opacity=0.2, annotation_text="Overweight")
            fig.add_hrect(y0=30, y1=50, line_width=0, fillcolor="red", opacity=0.2, annotation_text="Obese")
            st.plotly_chart(fig, use_container_width=True)

        # Show Data
        with st.expander("📂 View Raw Data"):
            st.dataframe(df)
    else:
        st.warning("No client data available.")

else:
    st.markdown(
        """
        <div style='text-align: center; padding: 30px; background-color: #2c2c2c; border-radius: 10px;'>
            <h2 style='color: #FF4B4B;'>⚠️ Access Denied</h2>
            <p style='color: #DDDDDD; font-size: 20px;'>Please <span style='color: #FF4B4B; font-weight: bold;'>Log In</span> to access Client Management features.</p>
        </div>
        """,
        unsafe_allow_html=True
    )