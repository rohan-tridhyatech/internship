import streamlit as st
import nltk
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

# Download necessary NLTK resources
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

# Initialize Stemmer and Lemmatizer
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

# Function to preprocess text
def preprocess_text(line, choice, case_option, remove_stopwords):
    # Case normalization
    if case_option == "Lower":
        line = line.lower()
    elif case_option == "Upper":
        line = line.upper()
    
    # Tokenization
    tokens = word_tokenize(line)
    
    # Remove Punctuation
    tokens_no_punct = [word for word in tokens if word not in string.punctuation]
    
    # Stop Word Removal (if enabled)
    if remove_stopwords:
        stop_words = set(stopwords.words("english"))
        filtered_tokens = [word for word in tokens_no_punct if word.lower() not in stop_words]
    else:
        filtered_tokens = tokens_no_punct

    # Apply Stemming or Lemmatization
    if choice == "Stemming":
        processed_tokens = [stemmer.stem(word) for word in filtered_tokens]
    else:
        processed_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
    
    # Join the processed tokens back into a single string
    return " ".join(processed_tokens)

def main():
    # Custom CSS and HTML for styling
    st.markdown("""
        <style>
        body {
            background-color: #f5f5f5;
            font-family: 'Arial', sans-serif;
        }
        .stApp {
            background: linear-gradient(to right, #f0f4f8, #d9e2ec);
            padding: 2rem;
        }
        .css-18e3th9 {
            padding: 2rem;
        }
        h1, h2, h3, h4 {
            color: #333333;
        }
        .stButton button {
            background-color: #007bff;
            color: white;
            font-size: 1rem;
            border-radius: 5px;
            padding: 0.5rem 1rem;
        }
        .stButton button:hover {
            background-color: #0056b3;
        }
        textarea {
            font-size: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("✨ Text Preprocessing Application")
    st.markdown("""
        <h3>🌟 Clean and prepare your text for analysis with ease!</h3>
        <p>Choose from a range of options to process text: case normalization, stop word removal, and applying either stemming or lemmatization.</p>
    """, unsafe_allow_html=True)

    # Sidebar: User options
    st.sidebar.header("🔧 Processing Options")
    case_option = st.sidebar.radio("Choose case normalization:", ("Lower", "Upper"))
    choice = st.sidebar.radio("Choose your text processing method:", ("Stemming", "Lemmatization"))
    remove_stopwords = st.sidebar.checkbox("Remove Stop Words", value=True)

    # Input Text
    input_text = st.text_area("📝 Enter text to preprocess (multiple lines supported):", height=200)

    if st.button("🚀 Process Text"):
        if not input_text.strip():
            st.warning("⚠️ Please enter some text.")
        else:
            # Split text into lines
            lines = input_text.split("\n")
            
            # Process each line and preserve formatting
            processed_lines = []
            for line in lines:
                if line.strip():  # Skip empty lines
                    processed_line = preprocess_text(line, choice, case_option, remove_stopwords)
                else:
                    processed_line = ""  # Preserve empty lines
                processed_lines.append(processed_line)

            # Combine processed lines into a single output with line breaks
            final_output = "\n".join(processed_lines)

            # Display the final output
            st.subheader("📜 Processed Text")
            st.markdown(f"<div style='padding:1rem; background:#e9ecef; border-radius:8px;'>{final_output}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
