import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from image_preprocessing import *


st.title("Image Filter Application")

# Sidebar options
st.sidebar.title("Options")
uploaded_image = st.sidebar.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])    
# # Additional Features
# join_option = st.sidebar.radio("Join Images", ["None", "Horizontal", "Vertical", "Both"])
# text_input = st.sidebar.text_input("Add Text to Image")
# text_color = st.sidebar.color_picker("Text Color", "#000000")
# shape_option = st.sidebar.radio("Add Shape", ["None", "Rectangle", "Circle", "Ellipse"])
# shape_color = st.sidebar.color_picker("Shape Color", "#FF0000")
# shape_coords = None
# if shape_option != "None":
#     shape_coords = st.sidebar.slider(f"Define {shape_option} Position", 0, 500, (100, 100))

if uploaded_image is not None:
    # Load the image using PIL and convert to OpenCV format
    image = Image.open(uploaded_image)
    original_width, original_height = image.size
    image_np = np.array(image)
        
    # Display the original image
    st.subheader("Original Image")
    st.image(image, caption="Uploaded Image", use_container_width=True)
    
    # Resize Image Inputs
    st.sidebar.subheader("Resize Image")
    resize = st.sidebar.checkbox("Enable Resize")
    resize_width = st.sidebar.slider("Width", min_value=1, max_value=original_width * 2, value=original_width)
    resize_height = st.sidebar.slider("Height", min_value=1, max_value=original_height * 2, value=original_height)
    filter_option = st.sidebar.selectbox("Choose a Filter", ["Original", "Grayscale", "Blur", "Edge Detection"])
    blur_ksize = st.sidebar.slider("Blur Kernel Size", min_value=3, max_value=15, step=2, value=5)
    edge_thresh1 = st.sidebar.slider("Edge Detection Threshold 1", min_value=50, max_value=300, step=10, value=100)
    edge_thresh2 = st.sidebar.slider("Edge Detection Threshold 2", min_value=50, max_value=300, step=10, value=200)

    # Resize the Image
    if resize:
        image_np = resize_image(image_np, int(resize_width), int(resize_height))
        # st.subheader("Resized Image")
        # st.image(image_np, caption=f"Resized to {resize_width}x{resize_height}", use_container_width=True)
    # Apply the selected filter
    processed_image = apply_filter(image_np, filter_option, blur_ksize, edge_thresh1, edge_thresh2)

#     # Add text if input is provided
#     if text_input:
#         processed_image = add_text_to_image(processed_image, text_input, text_color)

#     # Add shape if selected
#     if shape_option != "None" and shape_coords:
#         processed_image = add_shape_to_image(processed_image, shape_option, shape_coords, shape_color)

#     # Join images horizontally or vertically if selected
#     if join_option != "None":
#         processed_image = join_images(processed_image, join_option)

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
