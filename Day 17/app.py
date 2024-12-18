import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Function to apply custom CSS
def apply_custom_css():
    st.markdown("""
        <style>
            /* General page styling */
            body {
                font-family: 'Arial', sans-serif;
                background-color: #f9f9f9;
                color: #333;
            }

            /* Header styling */
            .main-header {
                background: linear-gradient(to right, #4CAF50, #0073e6);
                color: white;
                padding: 15px;
                text-align: center;
                font-size: 2.5rem;
                font-weight: bold;
                border-radius: 10px;
                margin-bottom: 20px;
            }

            /* Footer styling */
            .footer {
                margin-top: 50px;
                text-align: center;
                color: #666;
                font-size: 0.9rem;
            }
            .footer a {
                color: #0073e6;
                text-decoration: none;
            }
            .footer a:hover {
                text-decoration: underline;
            }

            /* Sidebar styling */
            [data-testid="stSidebar"] {
                background: linear-gradient(to bottom, #ffffff, #e6f7ff);
                padding: 20px;
                border-right: 2px solid #ccc;
                border-radius: 5px;
            }

            /* Widget alignment */
            .stSlider, .stTextInput, .stSelectbox, .stColorPicker {
                margin-bottom: 15px;
            }

            /* Button styling */
            button[data-testid="stDownloadButton"] {
                background: linear-gradient(to right, #0073e6, #4CAF50);
                color: white;
                border-radius: 5px;
                font-size: 16px;
                padding: 10px;
            }
            button[data-testid="stDownloadButton"]:hover {
                background: linear-gradient(to right, #005bb5, #388e3c);
            }

            /* Image styling */
            img {
                display: block;
                margin: 20px auto;
                border-radius: 15px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }

            /* Section titles */
            .section-title {
                font-size: 1.8rem;
                color: #0073e6;
                text-align: center;
                margin-top: 30px;
                margin-bottom: 20px;
            }
        </style>
    """, unsafe_allow_html=True)

# Resize image
def resize_image(image, width, height):
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
    
# Apply filters
def apply_filter(image, filter_option, blur_ksize, edge_thresh1, edge_thresh2):
    if filter_option == "Grayscale":
        return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    elif filter_option == "Blur":
        return cv2.GaussianBlur(image, (blur_ksize, blur_ksize), 0)
    elif filter_option == "Edge Detection":
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, threshold1=edge_thresh1, threshold2=edge_thresh2)
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
    return image

# Add text to image
def add_text_to_image(image, text, org, color):
    return cv2.putText(image, text, org, cv2.FONT_HERSHEY_DUPLEX, 3, color, 3, cv2.LINE_AA, False)

# Convert image to bytes for download
def convert_image_to_bytes(image):
    from io import BytesIO
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.read()

# Main function
def main():
    apply_custom_css()  # Apply custom CSS

    # Header
    st.markdown('<div class="main-header">✨ Image Filter Application ✨</div>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("Upload & Customize")
    uploaded_image = st.sidebar.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])    

    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        original_width, original_height = image.size
        image_np = np.array(image)
        
        st.markdown('<div class="section-title">Original Image</div>', unsafe_allow_html=True)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        
        # Sidebar widgets
        resize_width = st.sidebar.slider("Resize Width", min_value=1, max_value=original_width * 2, value=original_width)
        resize_height = st.sidebar.slider("Resize Height", min_value=1, max_value=original_height * 2, value=original_height)
        filter_option = st.sidebar.selectbox("Choose a Filter", ["Original", "Grayscale", "Blur", "Edge Detection"])
        blur_ksize = st.sidebar.slider("Blur Kernel Size", min_value=3, max_value=15, step=2, value=5)
        edge_thresh1 = st.sidebar.slider("Edge Detection Threshold 1", min_value=50, max_value=300, step=10, value=100)
        edge_thresh2 = st.sidebar.slider("Edge Detection Threshold 2", min_value=50, max_value=300, step=10, value=200)
        
        text_input = st.sidebar.text_input("Add Text to Image")
        text_color = st.sidebar.color_picker("Text Color", "#000000")
        text_X_org = st.sidebar.slider("Text X axis Position", min_value=0, max_value=original_width, step=10, value=original_width//2)
        text_Y_org = st.sidebar.slider("Text Y axis Position", min_value=0, max_value=original_height, step=10, value=original_height//2)

        # Process the image
        processed_image = resize_image(image_np, int(resize_width), int(resize_height))
        processed_image = apply_filter(processed_image, filter_option, blur_ksize, edge_thresh1, edge_thresh2)

        # Add text
        if text_input:
            text_color = tuple(int(text_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
            processed_image = add_text_to_image(processed_image, text_input, (text_X_org, text_Y_org), text_color)

        st.markdown('<div class="section-title">Processed Image</div>', unsafe_allow_html=True)
        st.image(processed_image, caption="Processed Image", channels="RGB", use_container_width=False)

        # Download button
        processed_pil = Image.fromarray(processed_image)
        st.sidebar.download_button(
            label="Download Processed Image",
            data=convert_image_to_bytes(processed_pil),
            file_name="processed_image.png",
            mime="image/png"
        )

    # Footer
    st.markdown("""
        <div class="footer">
            Built with ❤️ using <a href="https://streamlit.io" target="_blank">Streamlit</a>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
