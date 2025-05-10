import streamlit as st
from database.db_connect import add_client, view_clients, delete_client, update_client,get_client_by_id
from database.diet_plan import load_diet_data,save_diet_data
from database.workout_manage import load_workouts,save_workouts
from database.progress import load_progress_data,save_progress_data
from database.phone import load_phone_data,save_phone_data
import json
from datetime import datetime
import pywhatkit as kit
import qrcode
from database.payment import load_payment_data,save_payment_data,update_payment,add_new_client

def add_phone(name, phone_no):
    data = load_phone_data()  # Load the existing phone data
    data[name] = phone_no  # Add or update the client's phone number
    save_phone_data(data)  # Save the updated data
# Page Config
st.set_page_config(page_title="Client Management", page_icon="🏋️‍♂️", layout="wide")
if st.session_state['logged_in'] == True:
    # Logo/Header
    st.markdown("""
        <h2 style='text-align: center; color: #4CAF50;'>🏋️ Personal Trainer Client Management 📝</h2>
        <hr>
    """, unsafe_allow_html=True)

    # Sidebar Navigation
    menu = st.sidebar.radio("Select Operation", ["📱 Connect with client", "➕ Add Client", "👀 View Clients", "✏️ Update Client", "🗑️ Delete Client","💰 Payment Request"])

    st.sidebar.markdown("---")
    st.sidebar.success("Logged in as: " + st.session_state['trainer_name'])

    # Home
    if menu == "📱 Connect with client":
        st.title("📱 Connect with Client on WhatsApp")

        # Load clients
        phone_data = load_phone_data()

        if not phone_data:
            st.warning("No clients found. Please add some clients first.")
        else:
            # Select client
            clients = view_clients(st.session_state['trainer_name'])
            client_names = [c[1] for c in clients]
            client_name = st.selectbox("Select a client to message 👇",client_names
                                       )

            if client_name:
                raw_phone = phone_data[client_name]
                # Remove '+' if present for pywhatkit
                phone_no = raw_phone.replace("+", "").strip()

                st.info(f"📞 Phone: {phone_no}")

                # Message input
                message = st.text_area("✍️ Enter your personalized message", f"Hi {client_name}, hope you are doing well!")

                if st.button("🚀 Send WhatsApp Message"):
                    try:
                        # Send instantly (with a wait time of 10-15 seconds for WhatsApp web to load)
                        kit.sendwhatmsg_instantly(f"+{phone_no}", message, wait_time=10, tab_close=True)
                        st.success(f"✅ WhatsApp message sent to {client_name}!")
                        st.info("ℹ️ Please make sure your WhatsApp Web is logged in for this to work.")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")

    # Add Client
    elif menu == "➕ Add Client":
        st.title("➕ Add New Client")
        st.markdown("Fill out the form below to register a new client to your list. 👇")

        st.markdown("---")

        # Form Layout
        with st.form(key="add_client_form"):
            col1, col2 = st.columns(2)

            with col1:
                name = st.text_input("👤 Client Name")
                age = st.number_input("🎂 Age", min_value=1, step=1)
                gender = st.selectbox("⚧️ Gender", ["Male", "Female", "Other"])
                phone_no = st.text_input("📞 Phone Number (with country code)", placeholder="+91XXXXXXXXXX")
            
            with col2:
                weight = st.number_input("⚖️ Weight (KG)", min_value=1.0, step=0.1)
                height = st.number_input("📏 Height (CM)", min_value=1.0, step=0.1)
                goal = st.text_input("🎯 Goal")
                amount=st.number_input("💵 Fees (INR)", min_value=1000)

            st.markdown("---")
            submitted = st.form_submit_button("✅ Add Client")
            if submitted:
                add_client(name, age, gender, weight, height, goal, st.session_state['trainer_name'])
                add_phone(name, phone_no)
                add_new_client(name,amount)
                st.success(f"✅ Client **{name}** added successfully!")

        st.markdown("---")
        st.info("📝 Make sure to fill out all fields correctly before submitting.")

    # View Clients
    elif menu == "👀 View Clients":
        st.subheader("👀 All Clients")

        clients = view_clients(st.session_state['trainer_name'])
        if clients:
            for c in clients:
                with st.container():
                    # Create two columns for side-by-side layout
                    col1, col2 = st.columns([1, 2])  # Ratio 1:2 for client info and payment info

                    # Client Information Section (Column 1)
                    with col1:
                        st.markdown(f"""
                            <div style="background-color: #2C2F33; border-left: 6px solid #00BFA5; padding: 20px; border-radius: 12px; box-shadow: 2px 4px 12px rgba(0,0,0,0.4);">
                                <h3 style="color: #FAFAFA; margin-bottom: 10px;">👤 <strong>{c[1]}</strong></h3>
                                <div style="color: #DDDDDD; font-size: 16px;">
                                    <p><strong>ID:</strong> {c[0]}</p>
                                    <p><strong>Age:</strong> {c[2]} years</p>
                                    <p><strong>Gender:</strong> {c[3]}</p>
                                    <p><strong>Weight:</strong> {c[4]} KG</p>
                                    <p><strong>Height:</strong> {c[5]} CM</p>
                                    <p><strong>Goal:</strong> {c[6]}</p>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)

                    # Payment Information Section (Column 2)
                    with col2:

                        # Fetch payment data
                        payment_data = None
                        payment_records = load_payment_data()
                        for record in payment_records["clients"]:
                            if record["client_name"].lower() == c[1].lower():
                                payment_data = record
                                break

                        if payment_data:
                            st.markdown(f"""
                            <div style="background-color: #2C2F33; padding: 20px; border-radius: 12px; box-shadow: 2px 4px 12px rgba(0,0,0,0.4);">
                                <h4 style="color: #FAFAFA;">💰 Payment Information for <strong>{c[1]}</strong></h4>
                                <div style="color: #DDDDDD; font-size: 16px;">
                                    <p><strong>Total Amount:</strong> ₹{payment_data['total_amount']}</p>
                                    <p><strong>Amount Paid:</strong> ₹{payment_data['amount_paid']}</p>
                                    <p><strong>Amount Due:</strong> ₹{payment_data['amount_due']}</p>
                                    <p><strong>Due Date:</strong> {payment_data['due_date']}</p>
                                    <p><strong>Status:</strong> 
                                        <span style="color: {'#4CAF50' if payment_data['payment_status'] == 'Paid' else '#F44336'};">
                                            {payment_data['payment_status']}
                                        </span>
                                    </p>
                                </div>
                                </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown("<p style='color: #F44336;'>No payment data found for this client.</p>", unsafe_allow_html=True)

                        st.markdown("</div>", unsafe_allow_html=True)

        else:
            st.warning("⚠️ No Clients Found!")


    # Update Client
    elif menu == "✏️ Update Client":
        st.title("✏️ Update Client Details")
        st.markdown("Select a client and update their details below. 👇")

        st.markdown("---")

        clients = view_clients(st.session_state['trainer_name'])
        client_ids = [c[0] for c in clients]

        selected_id = st.selectbox("🔎 Select Client ID", client_ids)

        client_info = get_client_by_id(selected_id)  # Fetch existing data
        existing_weight = client_info[4]  # Assuming weight at index 4

        with st.form(key="update_client_form"):
            col1, col2 = st.columns(2)

            with col1:
                name = st.text_input("👤 Updated Name", value=client_info[1])
                age = st.number_input("🎂 Updated Age", min_value=1, value=client_info[2], step=1)
                gender = st.selectbox(
                    "⚧️ Updated Gender",
                    ["Male", "Female", "Other"],
                    index=["Male", "Female", "Other"].index(client_info[3])
                )
                temp=load_phone_data()
                phone_no = st.text_input("📞 Phone Number (with country code)", placeholder="+91XXXXXXXXXX",value=temp[client_info[1]])

            with col2:
                weight = st.number_input("⚖️ Updated Weight (KG)", min_value=1.0, value=existing_weight, step=0.1)
                height = st.number_input("📏 Updated Height (CM)", min_value=1.0, value=client_info[5], step=0.1)
                goal = st.text_input("🎯 Updated Goal", value=client_info[6])

            st.markdown("---")
            submitted = st.form_submit_button("✅ Update Client")

            if submitted:
                update_client(selected_id, name, age, gender, weight, height, goal)
                st.success(f"✅ Client **{name}** updated successfully!")


                # Check if weight changed
                if weight != existing_weight:
                    with open('client_progress.json', 'r') as file:
                        progress_data = json.load(file)

                    client_name = client_info[1]  # Old name for tracking

                    if client_name not in progress_data:
                        progress_data[client_name] = [{
                            "date": datetime.now().strftime("%Y-%m-%d"),
                            "weight": weight,
                            "height": height
                        }]

                    # Append new weight entry
                    progress_data[client_name].append({
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "weight": weight,
                        "height": height
                    })

                    with open('client_progress.json', 'w') as file:
                        json.dump(progress_data, file, indent=4)

                add_phone(name, phone_no)

        st.markdown("---")
        st.info("📝 Remember: Changing the weight will automatically log the update in the client progress tracker!")

    # Delete Client
    elif menu == "🗑️ Delete Client":
        st.title("🗑️ Delete Client")
        st.markdown("Select a client to view details before deleting. ❗")

        st.markdown("---")

        clients = view_clients(st.session_state['trainer_name'])
        client_ids = [c[0] for c in clients]

        selected_id = st.selectbox("🔎 Select Client ID to Delete", client_ids)

        client_info = get_client_by_id(selected_id)

        if client_info:
            # Display client info in block style
            st.markdown("### 📝 Client Information")
            with st.container():
                st.markdown(f"""
                    <div style='background-color:#2C2F33; padding:20px; border-radius:10px; border:1px solid #ddd;'>
                        <h4>👤 {client_info[1]}</h4>
                        <p>🎂 Age: {client_info[2]}</p>
                        <p>⚧️ Gender: {client_info[3]}</p>
                        <p>⚖️ Weight: {client_info[4]} KG</p>
                        <p>📏 Height: {client_info[5]} CM</p>
                        <p>🎯 Goal: {client_info[6]}</p>
                    </div>
                """, unsafe_allow_html=True)

                # Display Payment Info
                st.markdown("### 💰 Payment Information")
                payment_data = None

                # Find payment record for the selected client
                payment_records = load_payment_data()
                for record in payment_records["clients"]:
                    if record["client_name"].lower() == client_info[1].lower():
                        payment_data = record
                        break

                if payment_data:
                    st.markdown(f"""
                        <div style='background-color:#2C2F33; padding:20px; border-radius:10px; border:1px solid #ddd;'>
                            <h4>💵 Payment Status for {client_info[1]}</h4>
                            <p>💰 Total Amount: ₹{payment_data['total_amount']}</p>
                            <p>💸 Amount Paid: ₹{payment_data['amount_paid']}</p>
                            <p>💳 Amount Due: ₹{payment_data['amount_due']}</p>
                            <p>📅 Due Date: {payment_data['due_date']}</p>
                            <p>Status: <span style="color:{'green' if payment_data['payment_status'] == 'Paid' else 'red'};">{payment_data['payment_status']}</span></p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning("No payment data found for this client.")

            st.markdown("    ")
            st.warning("⚠️ Deleting this client will also remove their diet, workout, and progress data.")

            if st.button("🗑️ Confirm Delete Client", use_container_width=True):
                # Delete client data
                client_name = client_info[1]
                try:
                    # Deleting client from main records
                    delete_client(selected_id)

                    # Load all relevant data
                    diet_data = load_diet_data()
                    workout_data = load_workouts()
                    progress = load_progress_data()
                    phone = load_phone_data()
                    payment = load_payment_data()

                    # Delete client's associated data from various JSON files

                    # Delete from Diet JSON
                    if client_name in diet_data:
                        del diet_data[client_name]
                        save_diet_data(diet_data)

                    # Delete from Workout JSON
                    if str(selected_id) in workout_data:
                        del workout_data[str(selected_id)]
                        save_workouts(workout_data)

                    # Delete from Progress JSON
                    if client_name in progress:
                        del progress[client_name]
                        save_progress_data(progress)

                    # Delete from Phone JSON
                    if client_name in phone:
                        del phone[client_name]
                        save_phone_data(phone)

                    # Delete from Payment JSON
                    if client_name in [c["client_name"] for c in payment["clients"]]:
                        payment["clients"] = [c for c in payment["clients"] if c["client_name"] != client_name]
                        save_payment_data(payment)

                    # Notify success
                    st.success(f"✅ Client **{client_name}** deleted successfully!")

                except Exception as e:
                    st.error(f"❌ Error while deleting the client: {str(e)}")

        else:
            st.error("Client not found.")

        st.sidebar.markdown("---")
        st.sidebar.button('🚪 Logout', on_click=lambda: st.session_state.update(logged_in=False, trainer_name=None), key='logout_button')




    # Payment Request Section
    elif menu == "💰 Payment Request":
        st.title("💰 Request Payment from Client")
        st.markdown("Use this section to send payment requests to your clients.")

        # Select Client for Payment Request
        clients = view_clients(st.session_state['trainer_name'])
        client_names = [c[1] for c in clients]
        client_name = st.selectbox("Select a client to request payment from 👇", client_names)

        if client_name:
            upiid = st.text_input("Enter receiver's UPI ID", placeholder="Trainer's UPI ID")
            amount = st.number_input("Enter Amount to Request (INR)", min_value=1.0, step=0.1)

            # Generate Payment Link and QR Code
            if amount > 0 and upiid:
                if st.button("Generate Payment Link"):
                    # Generate UPI link
                    upi_link = f"upi://pay?pa={upiid}&pn={st.session_state['trainer_name']}&mc=123456&amt={amount}&cu=INR"
                    
                    # Generate the QR code
                    qr = qrcode.make(upi_link)

                    # Convert the QR code to a PIL Image object
                    pil_img = qr.convert("RGB")  # Ensure the image is in RGB format

                    # Create two columns for displaying the QR code and the payment link
                    col1, col2 = st.columns(2)

                    # Display QR code in the first column
                    with col1:
                        st.image(pil_img, caption="Scan this QR code to make the payment", width=200)

                    # Display payment link in the second column
                    with col2:
                        st.markdown(f"**Payment Link**: [Click here to pay]({upi_link})")
                        st.text_area("Copy the link to share with the client", value=upi_link, height=100)

                    st.success(f"📈 Payment Request generated for **{client_name}**!")

            # Once the payment is made, update payment status
            if st.button("💸 Payment Successfully Received"):
                if amount > 0:
                    # Update payment record using the function
                    if update_payment(client_name, amount):
                        st.success(f"✅ Payment for **{client_name}** marked as successfully received!")
                    else:
                        st.error(f"❌ Payment record not found for **{client_name}**.")
                else:
                    st.error("❌ Invalid amount entered for payment update.")

        st.markdown("---")
        st.info("💡 You can share the payment link or the QR code with your client.")
    st.sidebar.button('Logout', on_click=lambda: st.session_state.update(logged_in=False, trainer_name=None))

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
