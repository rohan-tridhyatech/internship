import streamlit as st
import cv2
import numpy as np
from PIL import Image

def main():
    st.title("Image Filter Application")

    # Sidebar options
    st.sidebar.title("Options")
    uploaded_image = st.sidebar.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
    filter_option = st.sidebar.selectbox(
        "Choose a Filter", ["Original", "Grayscale", "Blur", "Edge Detection"]
    )
    blur_ksize = st.sidebar.slider("Blur Kernel Size", min_value=3, max_value=15, step=2, value=5)
    edge_thresh1 = st.sidebar.slider("Edge Detection Threshold 1", min_value=50, max_value=300, step=10, value=100)
    edge_thresh2 = st.sidebar.slider("Edge Detection Threshold 2", min_value=50, max_value=300, step=10, value=200)

    if uploaded_image is not None:
        # Load the image using PIL and convert to OpenCV format
        image = Image.open(uploaded_image)
        image_np = np.array(image)
        
        # Display the original image
        st.subheader("Original Image")
        st.image(image, caption="Uploaded Image", use_container_width=True)

        # Apply the selected filter
        processed_image = apply_filter(image_np, filter_option, blur_ksize, edge_thresh1, edge_thresh2)

        # Display the processed image
        st.subheader("Processed Image")
        st.image(processed_image, channels="RGB", use_container_width=True)

        # Download option for processed image
        processed_pil = Image.fromarray(processed_image)
        st.sidebar.download_button(
            label="Download Processed Image",
            data=convert_image_to_bytes(processed_pil),
            file_name="processed_image.png",
            mime="image/png"
        )

def apply_filter(image, filter_option, blur_ksize, edge_thresh1, edge_thresh2):
    # Convert to grayscale for processing
    if filter_option == "Grayscale":
        return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # Apply Gaussian Blur
    elif filter_option == "Blur":
        return cv2.GaussianBlur(image, (blur_ksize, blur_ksize), 0)

    # Apply Edge Detection
    elif filter_option == "Edge Detection":
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, threshold1=edge_thresh1, threshold2=edge_thresh2)
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)

    # Return original image if no filter is applied
    return image

def convert_image_to_bytes(image):
    from io import BytesIO
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.read()

if __name__ == "__main__":
    main()
