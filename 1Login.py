import streamlit as st
from database.db_connect import get_connection

# Admin Credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin"

# Sidebar Support Info
st.sidebar.markdown("Need Help? Contact Support👇")
st.sidebar.markdown("📞 +91-9876543210")  
st.sidebar.markdown("📧 trainerapp@gmail.com")
st.sidebar.markdown("🌐 www.trainerapp.com")
st.sidebar.markdown("---")

# CSS Styling
st.markdown("""
    <style>
        .login-container {
            background-color: #f5f7fa;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
            width: 400px;
            margin: auto;
            margin-top: 20px;
        }
        .login-header {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #2c3e50;
        }
        .custom-input {
            width: 100%;
            padding: 10px;
            margin-top: 10px;
            margin-bottom: 20px;
            border-radius: 8px;
            border: 1px solid #ddd;
            font-size: 16px;
        }
        .login-btn {
            background-color: #2980b9;
            color: white;
            padding: 10px;
            border: none;
            width: 100%;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
        }
        .login-btn:hover {
            background-color: #3498db;
        }
    </style>
""", unsafe_allow_html=True)

# Heading Outside the Login Box
st.markdown('<div class="login-header">Personal Trainer Login</div>', unsafe_allow_html=True)


email = st.text_input("Enter Email", placeholder="trainer@gmail.com")
password = st.text_input("Enter Password", type="password", placeholder="Enter your password")


# Login Function
def login(email, password):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM trainer WHERE email=? AND password=?"
    cursor.execute(query, (email, password))
    data = cursor.fetchone()
    conn.close()
    return bool(data)

# Login Button
if st.button("Login", key="login_btn"):
    if email == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        st.session_state['is_admin'] = True
        st.success("✅ Logged in as Admin!")
    
    elif login(email, password):
        st.success("✅ Login Successful!")

        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT name FROM trainer WHERE email=?"
        cursor.execute(query, (email,))
        data = cursor.fetchone()
        conn.close()

        if data:
            st.session_state['trainer_name'] = data[0]
        else:
            st.session_state['trainer_name'] = "trainer_username"
        st.session_state['logged_in'] = True

    else:
        st.error("❌ Invalid Email or Password!")
