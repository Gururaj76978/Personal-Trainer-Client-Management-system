import streamlit as st
from database.trainer_manage import view_trainers,add_trainer,delete_trainer,update_trainer
st.markdown("""
    <style>
        /* Global Styles */
        body {
            font-family: 'Arial', sans-serif;
            background-color: #121212;  /* Dark background */
            color: #f1f1f1; /* Light text color */
            margin: 0;
            padding: 0;
        }

        /* Sidebar Styling */
        .sidebar .sidebar-content {
            background-color: #1e1e1e;  /* Dark sidebar background */
            color: #fff;
            padding: 20px;
            border-radius: 8px;
        }

        .sidebar .sidebar-content h2 {
            color: #fff;
            font-size: 1.5rem;
            margin-bottom: 30px;
        }

        .sidebar .sidebar-content .stButton>button {
            background-color: #007BFF;
            color: white;
            border-radius: 4px;
            font-size: 16px;
            padding: 12px 20px;
            width: 100%;
            border: none;
            cursor: pointer;
        }

        .sidebar .sidebar-content .stButton>button:hover {
            background-color: #0056b3;
        }

        /* Header */
        .header {
            background-color: #1e2a36;  /* Dark header */
            color: white;
            padding: 25px;
            text-align: center;
            font-size: 2rem;
            margin-bottom: 20px;
            border-radius: 8px;
            margin-top: 20px;
        }

        /* Main Container */
        .main-container {
            background-color: #2e2e2e; /* Dark background for main container */
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
            margin-bottom: 30px;
        }

        /* Buttons */
        .stButton>button {
            background-color: #28a745;
            color: white;
            padding: 12px 24px;
            font-size: 16px;
            border-radius: 4px;
            border: none;
            cursor: pointer;
            width: 100%;
        }

        .stButton>button:hover {
            background-color: #218838;
        }

        /* Form Fields */
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            background-color: #333;  /* Dark background for input fields */
            color: #f1f1f1;  /* Light text color */
            padding: 12px;
            font-size: 16px;
            border-radius: 4px;
            border: 1px solid #444;
            width: 100%;
            margin-bottom: 15px;
        }

        /* Tables */
        .stTable>div>table {
            width: 100%;
            border-collapse: collapse;
        }

        .stTable>div>table th, .stTable>div>table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #444;
        }

        .stTable>div>table th {
            background-color: #444;
            color: #f1f1f1;
        }

        .stTable>div>table td {
            background-color: #333;
        }

        /* Success and Error Messages */
        .success {
            color: #28a745;
            font-weight: bold;
        }

        .error {
            color: #dc3545;
            font-weight: bold;
        }

    </style>
""", unsafe_allow_html=True)

# Check if the user is an admin
if 'is_admin' in st.session_state and st.session_state['is_admin'] == True:
    # Header of the Admin Dashboard
    st.markdown('<div class="header"><h2>🛠️ Admin Dashboard - Trainer Management</h2></div>', unsafe_allow_html=True)

    # Sidebar for logout and navigation menu
    st.sidebar.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.sidebar.button("🚪 Logout", on_click=lambda: st.session_state.update(is_admin=False, logged_in=False), key='logout_button')
    st.sidebar.markdown('---')
    
    # Sidebar menu for different operations
    menu = st.sidebar.selectbox("🎯 Choose Trainer Operation", ["Add Trainer", "View Trainers", "Update Trainer", "Delete Trainer"])
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

    # Main Content Container
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # Add Trainer Section
    if menu == "Add Trainer":
        with st.form(key="add_trainer_form"):
            name = st.text_input("Enter Trainer's Full Name:")
            username = st.text_input("Create a Username:")
            password = st.text_input("Create a Password:", type="password")
            submit_button = st.form_submit_button(label="Add Trainer")

            if submit_button:
                if not name or not username or not password:
                    st.markdown('<p class="error">❌ All fields are required!</p>', unsafe_allow_html=True)
                else:
                    add_trainer(name, username, password)
                    st.markdown('<p class="success">✅ Trainer Added Successfully!</p>', unsafe_allow_html=True)

    # View Trainers Section
    elif menu == "View Trainers":
        trainers = view_trainers()
        if trainers:
            st.table([{"ID": t[0], "Name": t[1], "Username": t[2]} for t in trainers])
        else:
            st.markdown('<p class="error">⚠️ No trainers found!</p>', unsafe_allow_html=True)

    # Update Trainer Section
    elif menu == "Update Trainer":
        trainers = view_trainers()
        if trainers:
            ids = [t[0] for t in trainers]
            selected_id = st.selectbox("Select Trainer to Update", ids)
            trainer_data = next(t for t in trainers if t[0] == selected_id)
            name = st.text_input("Updated Name", trainer_data[1])
            username = st.text_input("Updated Username", trainer_data[2])
            password = st.text_input("Updated Password", type="password")

            if st.button("Update"):
                if not name or not username or not password:
                    st.markdown('<p class="error">❌ All fields are required!</p>', unsafe_allow_html=True)
                else:
                    update_trainer(selected_id, name, username, password)
                    st.markdown('<p class="success">✅ Trainer Updated Successfully!</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="error">⚠️ No trainers available to update.</p>', unsafe_allow_html=True)

    # Delete Trainer Section
    elif menu == "Delete Trainer":
        trainers = view_trainers()
        if trainers:
            ids = [t[0] for t in trainers]
            selected_id = st.selectbox("Select Trainer to Delete", ids)

            if st.button("Delete"):
                delete_trainer(selected_id)
                st.markdown('<p class="success">✅ Trainer Deleted Successfully!</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="error">⚠️ No trainers available to delete.</p>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Page Config
    #st.set_page_config(page_title="Personal Trainer Client Management", page_icon="💪", layout="wide")

    st.sidebar.image("assets/logo.png", use_container_width=True)
    if 'logged_in' in st.session_state:
        pass
    else:
        st.session_state['logged_in'] = False
    # Title Section
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>💪 Personal Trainer Client Management System</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: grey;'>Manage your clients, diet plans, workout routines, and performance effortlessly!</h4>", unsafe_allow_html=True)

    st.markdown("---")

    # Features Section
    st.subheader("🚀 Features Available:")

    col1, col2 = st.columns(2)

    with col1:
        st.success("🔐 Trainer Login\n\nSecure login to access your dashboard and manage clients.")

        st.info("👤 Client Management\n\nAdd, view, update, and delete client details like goals and personal info")

        st.warning("🥗 Diet Plan Management\n\nCreate personalized diet plans for each client.")

    with col2:
        st.success("🏋️ Workout Plan Management\n\nCreate and assign customized workout plans.")

        st.info("📊 Performance Analysis\n\nTrack client progress with charts and reports.")

        st.warning("⚙️ Settings & Profile\n\nManage your profile and system settings.")

    st.markdown("---")

    # Call to Action
    st.markdown("<h3 style='text-align: center;'>Start Managing Your Clients Now! 🚀</h3>", unsafe_allow_html=True)

    st.markdown("<p style='text-align: center;'>Login from the sidebar to get started.</p>", unsafe_allow_html=True)

    st.markdown("---")

    # Footer
    st.markdown("<p style='text-align: center; color: grey;'>Developed by Gururaj | Powered by Streamlit ❤️</p>", unsafe_allow_html=True)
