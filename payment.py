import streamlit as st
import qrcode

# Function to generate UPI payment link
def generate_upi_link(upiid, name, amount):
    txn_id = "TXN123456"  # Ideally, generate a unique transaction ID
    upi_link = f"upi://pay?pa={upiid}&pn={name}&mc=123456&tid={txn_id}&txn={txn_id}&amt={amount}&cu=INR"
    return upi_link

# Function to generate and display QR code
def generate_qr_code(upi_link):
    qr = qrcode.make(upi_link)
    return qr

# Streamlit UI elements
st.title("UPI Payment Generator")

# Input for UPI ID and Name
upiid = st.text_input("Enter UPI ID (Payee UPI)", "merchant@upi")
name = st.text_input("Enter Payee Name", "Merchant Name")
amount = st.number_input("Enter Amount (INR)", min_value=1.0, step=0.01)

# Generate UPI link and QR code when user clicks the button
if st.button("Generate UPI Link and QR Code"):
    if upiid and name and amount:
        upi_link = generate_upi_link(upiid, name, amount)
        qr_code = generate_qr_code(upi_link)
        
        st.success(f"Generated UPI Payment Link: {upi_link}")
        st.markdown(f"[Click here to make payment]({upi_link})", unsafe_allow_html=True)
        
        st.image(qr_code, caption="Scan this QR code to make payment", use_column_width=True)
    else:
        st.error("Please fill in all fields")
