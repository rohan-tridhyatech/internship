import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Function to detect faces in an image
def detect_faces(image):
    gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    face_cascade = cv2.CascadeClassifier(r"env\\Lib\site-packages\\cv2\data\\haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return faces

# Convert image to bytes for download
def convert_image_to_bytes(image):
    from io import BytesIO
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.read()

# Streamlit UI with improved styling and emojis
st.title("🎨 Face Detection Tool 📷")
st.markdown("""
<style>
    .main {
        background-color: #f0f8ff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        font-family: 'Arial', sans-serif;
    }
    h1, h3, p {
        text-align: center;
    }
    .stImage img {
        border-radius: 10px;
        border: 2px solid #00aaff;
    }
    .stDownload button {
        background-color: #007bff;
        color: white;
        border-radius: 5px;
        padding: 12px 24px;
        font-size: 16px;
        cursor: pointer;
    }
    .stDownload button:hover {
        background-color: #0056b3;
    }
</style>
""", unsafe_allow_html=True)

st.write("👋 Upload an image to detect faces and enhance your visuals 🌟")

# File uploader
uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    image = Image.open(uploaded_image)

    # Display original image
    st.image(image, caption="📸 Uploaded Image", use_container_width=True)

    # Detect faces
    faces = detect_faces(image)

    # Draw rectangles around detected faces
    image_with_faces = np.array(image)
    for (x, y, w, h) in faces:
        cv2.rectangle(image_with_faces, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display processed image with detected faces
    st.image(image_with_faces, caption="🤳 Faces Detected", use_container_width=True)

    # Allow downloading the processed image
    processed_pil = Image.fromarray(image_with_faces)
    st.download_button(
        label="📥 Download Processed Image",
        data=convert_image_to_bytes(processed_pil),
        file_name="processed_image.png",
        mime="image/png"
    )
