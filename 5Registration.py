import streamlit as st
from database.db_connect import get_connection

# Sidebar Support Info
st.sidebar.markdown("Need Help? Contact Support👇")
st.sidebar.markdown("📞 +91-9876543210")  
st.sidebar.markdown("📧 trainerapp@gmail.com")
st.sidebar.markdown("🌐 www.trainerapp.com")
st.sidebar.markdown("---")



st.markdown("""
    <style>
        .registration-container {
            background-color: #f9f9f9;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            width: 400px;
            margin: auto;
            margin-top: 50px;
        }
        .registration-header {
            text-align: center;
            font-size: 30px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 30px;
        }
        .custom-input {
            width: 100%;
            padding: 12px;
            margin-bottom: 20px;
            border-radius: 8px;
            border: 1px solid #ccc;
            font-size: 16px;
        }
        .register-btn {
            background-color: #27ae60;
            color: white;
            padding: 12px;
            width: 100%;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
        }
        .register-btn:hover {
            background-color: #2ecc71;
        }
    </style>
""", unsafe_allow_html=True)

# Heading
st.markdown('<div class="registration-header">Trainer Registration</div>', unsafe_allow_html=True)

# Inputs
name = st.text_input("Enter Name", placeholder="Full Name")
email = st.text_input("Enter Email", placeholder="trainer@gmail.com")
password = st.text_input("Enter Password", type="password", placeholder="Choose Strong Password")

# DB Function
def add_trainer(name, email, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO trainer (name, email, password) VALUES (?, ?, ?)", 
                       (name, email, password))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

# Button
if st.button("Register", key="register_btn"):
    if name == "" or email == "" or password == "":
        st.warning("Please fill all the details!")
    elif add_trainer(name, email, password):
        st.success("Registration Successful! Now Login.")
    else:
        st.error("Email Already Registered!")

# Close Container Div
st.markdown("</div>", unsafe_allow_html=True)
