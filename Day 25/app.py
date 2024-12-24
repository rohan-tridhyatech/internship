import streamlit as st
import requests

# Base URL of the FastAPI server
api_url = "http://127.0.0.1:5000"

# Title of the Streamlit app with custom styling and emojis
st.markdown("<h1 style='text-align: center; color: #007bff;'>🌟 Real-Time Sentiment Analysis Dashboard 🌟</h1>", unsafe_allow_html=True)

# Using Bootstrap for a modern, attractive, and responsive UI
st.markdown("""
    <style>
        .stTextArea textarea {
            width: 100%;
            height: 200px;
            resize: none;
            border-radius: 5px;
            border: 1px solid #ced4da;
            padding: 10px;
        }
        .stButton>button {
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
        }
        .stButton>button:hover {
            background-color: #0056b3;
        }
        .sidebar {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .sidebar h4 {
            color: #495057;
        }
        .container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .result-card {
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            padding: 20px;
            margin-top: 20px;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar for input type selection
st.sidebar.markdown("<div class='sidebar'>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='color: #495057;'>Choose Input Type</h4>", unsafe_allow_html=True)
input_type = st.sidebar.radio("Input Type:", ["Single Text", "Batch Text"])
st.sidebar.markdown("</div>", unsafe_allow_html=True)

# Input form based on the selected type
if input_type == "Single Text":
    text_input = st.text_area("Enter your text for sentiment analysis:", height=200)
    if st.button("📈 Analyze Sentiment"):
        if text_input:
            payload = {"text": text_input}
            response = requests.post(f"{api_url}/predict/", json=payload)
            if response.status_code == 200:
                result = response.json()
                with st.container():
                    st.success(f"Sentiment: {result['sentiment']} 😊")
            else:
                st.error("Error in sentiment analysis. Please try again.")
        else:
            st.warning("Please enter some text to analyze. 🙃")

elif input_type == "Batch Text":
    texts_input = st.text_area("Enter multiple lines of text for sentiment analysis (each line separated by a newline):", height=200)
    if st.button("📊 Analyze Batch Sentiment"):
        if texts_input:
            input_lines = texts_input.split("\n")
            payload = [{"text": line.strip()} for line in input_lines if line.strip()]
            response = requests.post(f"{api_url}/predict_batch/", json=payload)
            if response.status_code == 200:
                results = response.json()
                with st.container():
                    for result in results["predictions"]:
                        st.success(f"Text: {result['text']} - Sentiment: {result['sentiment']} 😊")
            else:
                st.error("Error in batch sentiment analysis. Please try again.")
        else:
            st.warning("Please enter some text to analyze. 🙃")

st.markdown("</div>", unsafe_allow_html=True)
