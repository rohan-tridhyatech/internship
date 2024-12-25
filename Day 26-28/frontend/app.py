import streamlit as st
from pathlib import Path
import random
import smtplib

# Placeholder for user database and OTP verification
USER_DB = {}
OTP_STORE = {}

# Function to send email (mockup)
def send_email(email, otp):
    st.write(f"Sending email to {email} with OTP: {otp}")
    # Use smtplib or an email-sending API in a real app

# Function to load and display HTML files
def load_html(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# Main function
def main():
    st.set_page_config(page_title="Authorization System", layout="centered")

    # Load CSS for styling
    css_path = Path("css/styles.css")
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as css_file:
            st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

    menu = ["Home", "Login", "Register"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        html_path = Path("html/home.html")
        if html_path.exists():
            st.markdown(load_html(html_path), unsafe_allow_html=True)
        else:
            st.subheader("Welcome to the Home Page")
            st.write("This is an attractive landing page for your app. Use the sidebar to navigate.")

    elif choice == "Register":
        html_path = Path("html/register.html")
        if html_path.exists():
            st.markdown(load_html(html_path), unsafe_allow_html=True)

        with st.form("register_form"):
            username = st.text_input("Username")
            email = st.text_input("Email")
            contact = st.text_input("Contact Number")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit = st.form_submit_button("Register")

            if submit:
                if password != confirm_password:
                    st.error("Passwords do not match")
                elif username in USER_DB:
                    st.error("Username already exists")
                else:
                    otp = random.randint(1000, 9999)
                    OTP_STORE[email] = otp
                    send_email(email, otp)
                    st.success("OTP sent to your email. Please verify.")

        otp_input = st.text_input("Enter OTP to Verify")
        verify_button = st.button("Verify OTP")

        if verify_button:
            if OTP_STORE.get(email) == int(otp_input):
                USER_DB[username] = {"email": email, "contact": contact, "password": password}
                st.success("Account created and verified successfully!")
            else:
                st.error("Invalid OTP")

    elif choice == "Login":
        html_path = Path("html/login.html")
        if html_path.exists():
            st.markdown(load_html(html_path), unsafe_allow_html=True)

        with st.form("login_form"):
            login_option = st.radio("Login with", ["Username", "Email"])
            identifier = st.text_input("Enter your Username or Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")

            if submit:
                if login_option == "Username" and identifier in USER_DB and USER_DB[identifier]["password"] == password:
                    st.success(f"Welcome {identifier}!")
                elif login_option == "Email":
                    otp = random.randint(1000, 9999)
                    OTP_STORE[identifier] = otp
                    send_email(identifier, otp)
                    st.success("OTP sent to your email. Please verify.")

                    otp_input = st.text_input("Enter OTP to Verify")
                    verify_button = st.button("Verify OTP")

                    if verify_button:
                        if OTP_STORE.get(identifier) == int(otp_input):
                            st.success("Login successful!")
                        else:
                            st.error("Invalid OTP")
                else:
                    st.error("Invalid Username/Email or Password")

if __name__ == "__main__":
    main()
