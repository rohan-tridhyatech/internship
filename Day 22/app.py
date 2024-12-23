import streamlit as st
import pickle
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt

# Load the trained model and vectorizer
with open("movie_review_sentiment_analysis_model.pkl", "rb") as file:
    model = pickle.load(file)

with open("count_vectorizer.pkl", "rb") as file:
    cv = pickle.load(file)  # Load the fitted CountVectorizer

# Streamlit app setup
st.set_page_config(page_title="Movie Review Sentiment Analysis", layout="centered")
st.title("🎥 Movie Review Sentiment Analysis")
st.markdown("Enter movie reviews below, and the model will predict their sentiment.")

# Custom CSS styling
st.markdown("""
    <style>
        .stTextArea textarea {
            font-size: 16px;
            padding: 15px;
            border-radius: 8px;
            border: 2px solid #ddd;
            width: 100%;
            height: 150px;
        }
        .stButton > button {
            background-color: #ff7f50;
            color: white;
            font-size: 16px;
            padding: 10px 20px;
            border-radius: 8px;
            border: none;
            cursor: pointer;
        }
        .stButton > button:hover {
            background-color: #ff6347;
        }
    </style>
""", unsafe_allow_html=True)

# Input field for user to enter multiple reviews
user_input = st.text_area("Movie Reviews (Separate each review with a newline)", placeholder="Type your movie reviews here...")

# Dropdown for graph choice
graph_choice = st.selectbox("Choose Visualization:", ["Select", "Bar Chart", "Pie Chart"])

# Predict button
if st.button("Predict Sentiments"):
    if user_input.strip():
        try:
            # Split input into multiple reviews
            reviews = user_input.split('\n')
            reviews = [review.strip() for review in reviews if review.strip()]
            
            # Transform the input data using the loaded CountVectorizer
            input_data_features = cv.transform(reviews)
            predictions = model.predict(input_data_features)
            sentiments = ["Positive" if pred == 1 else "Negative" for pred in predictions]
            
            # Create a DataFrame for visualization
            df = pd.DataFrame({'Review': reviews, 'Sentiment': sentiments})
            sentiment_counts = df['Sentiment'].value_counts()
            
            # Display individual review sentiments
            st.subheader("Sentiments for Each Review")
            st.write(df)
            
            if graph_choice == "Bar Chart":
                st.subheader("Sentiment Distribution - Bar Chart")
                fig, ax = plt.subplots()
                sentiment_counts.plot(kind='bar', ax=ax, color=['#4CAF50', '#FF6347'])
                ax.set_title('Sentiment Distribution')
                ax.set_xlabel('Sentiment')
                ax.set_ylabel('Count')
                st.pyplot(fig)
            
            elif graph_choice == "Pie Chart":
                st.subheader("Sentiment Distribution - Pie Chart")
                fig, ax = plt.subplots()
                sentiment_counts.plot(kind='pie', autopct='%1.1f%%', colors=['#4CAF50', '#FF6347'], ax=ax, legend=False)
                ax.set_title('Sentiment Distribution')
                ax.set_ylabel('')  # Remove y-label for pie chart
                st.pyplot(fig)
        
        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")
    else:
        st.warning("Please enter valid reviews to analyze.")
