import streamlit as st
import requests
from streamlit_option_menu import option_menu 


# Base URL of your Django API
API_BASE_URL = "http://127.0.0.1:8000/"

# CSS for styling
st.markdown("""
    <style>
        body {
            background-color: #f8f9fa;
            font-family: 'Arial', sans-serif;
        }
        .main-container {
            background: #ffffff;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        .stButton > button {
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
        }
        .stButton > button:hover {
            background-color: #0056b3;
            cursor: pointer;
        }
        .stRadio > div {
            display: flex;
            justify-content: space-around;
            gap: 10px;
        }
        .stRadio > div > label {
            font-size: 18px;
            color: #007bff;
        }
        .title {
            font-size: 2.5rem;
            font-weight: bold;
            color: #007bff;
            margin-bottom: 20px;
            text-align: center;
        }
        .subheader {
            font-size: 1.5rem;
            color: #343a40;
            margin-bottom: 1.5rem;
        }
    </style>
""", unsafe_allow_html=True)

def login():
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
    st.markdown("<h2 class='subheader'>Login</h2>", unsafe_allow_html=True)

#     # Login options
#     login_method = st.radio("Choose your login method:", ("Username & Password", "Email Verification"))
      
    # Option menu for login method
    login_method = option_menu(
        menu_title=None,  # No menu title
        options=["Username & Password", "Email Verification"],  # Menu options
        icons=["person", "envelope"],  # Icons for each option
        default_index=0,  # Default selected index
        orientation="horizontal",  # Horizontal orientation
        styles={
            "container": {"padding": "0", "background-color": "#f8f9fa"},
            "nav-link": {
                "font-size": "18px",
                "font-weight": "bold",
                "color": "#007bff",
                "text-align": "center",
                "margin": "0px",
            },
            "nav-link-selected": {"background-color": "#007bff", "color": "white"},
        },
    )


    # Login using Username & Password
    if login_method == "Username & Password":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if not username or not password:
                st.error("Both username and password are required!")
                return

            data = {"username": username, "password": password}
            response = requests.post(f"{API_BASE_URL}/username-login/", data=data)

            if response.status_code == 200:
                st.success("Login Successful!")
            else:
                error_message = response.json().get("error", "Invalid username or password.")
                st.error(error_message)

    # Login using Email Verification
    elif login_method == "Email Verification":
        email = st.text_input("Email")

        if st.button("Send Verification Code"):
            if not email:
                st.error("Email is required!")
                return

            data = {"email": email}
            response = requests.post(f"{API_BASE_URL}/email-login/", data=data)

            if response.status_code == 200:
                st.success("Verification code sent to your email!")
                st.session_state.email_sent = True
            else:
                error_message = response.json().get("error", "Failed to send verification code. Please try again.")
                st.error(error_message)

        # Email OTP Verification
        if st.session_state.get("email_sent", False):
            otp = st.text_input("Enter OTP")
            if st.button("Verify OTP"):
                if not otp:
                    st.error("OTP is required!")
#                     return

                data = {"email": email, "otp": otp}
                verify_response = requests.post(f"{API_BASE_URL}/verify-email-login/", data=data)

                if verify_response.status_code == 200:
                    st.success("Email Verified Successfully! Login Successful!")
                else:
                    error_message = verify_response.json().get("error", "Invalid OTP. Please try again.")
                    st.error(error_message)
    st.markdown("</div>", unsafe_allow_html=True)

def register():
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
    st.markdown("<h2 class='subheader'>Register</h2>", unsafe_allow_html=True)

    username = st.text_input("Username")
    email = st.text_input("Email")
    contact = st.text_input("Contact Number")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if not username or not email or not contact or not password:
            st.error("All fields are required!")
            return

        data = {"username": username, "email": email, "password": password, "contact": contact}
        response = requests.post(f"{API_BASE_URL}/register/", data=data)

        if response.status_code == 201:
            st.success("Registration Successful! Verifying your email with OTP...")
            st.session_state.otp_sent = True
        else:
            error_message = response.json().get("error", "Failed to register. Please try again.")
            st.error(error_message)

    if st.session_state.get("otp_sent", False):
        otp = st.text_input("Enter OTP")
        if st.button("Verify OTP"):
            data = {"email": email, "otp": otp}
            verify_response = requests.post(f"{API_BASE_URL}/verify-otp/", data=data)

            if verify_response.status_code == 200:
                st.success("Email Verified Successfully!")
            else:
                error_message = verify_response.json().get("error", "Invalid OTP. Please try again.")
                st.error(error_message)
    st.markdown("</div>", unsafe_allow_html=True)

def image_processing():
    pass

def movie_recommendation():
    pass


def main():
    st.markdown("<div class='title'>Django Auth API Frontend</div>", unsafe_allow_html=True)

    # Use option_menu for navigation
    menu = option_menu(
        menu_title=None,  # No menu title
        options=["Register", "Login", "Movies","Image"],  # Menu options
        icons=["person-plus", "key", "film", "image"],  # Icons for each option
        default_index=1,  # Default to "Login"
        orientation="horizontal",  # Horizontal layout
        styles={
            "container": {"padding": "0", "background-color": "#f8f9fa"},
            "nav-link": {
                "font-size": "18px",
                "font-weight": "bold",
                "color": "#007bff",
                "text-align": "center",
                "margin": "0px",
            },
            "nav-link-selected": {"background-color": "#007bff", "color": "white"},
        },
    )

    if menu == "Login":
        login()
    elif menu == "Register":
        register()
    elif menu == "Movies":
        movie_recommendation()  
    elif menu == "Image":
        image_processing()


if __name__ == "__main__":
    main()

