import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def resize_image(image, width, height):
    resized_image =  cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
    return resized_image
 

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

def add_text_to_image(image, text, color):
    image_pil = Image.fromarray(image)
    draw = ImageDraw.Draw(image_pil)
    font = ImageFont.load_default()
    width, height = image_pil.size
    text_x = width // 2
    text_y = height // 2
    draw.text((text_x, text_y), text, fill=color, anchor="mm", font=font)
    return np.array(image_pil)

def add_shape_to_image(image, shape, coords, color):
    image_pil = Image.fromarray(image)
    draw = ImageDraw.Draw(image_pil)
    if shape == "Rectangle":
        draw.rectangle([coords[0]-50, coords[1]-50, coords[0]+50, coords[1]+50], outline=color, width=3)
    elif shape == "Circle":
        draw.ellipse([coords[0]-50, coords[1]-50, coords[0]+50, coords[1]+50], outline=color, width=3)
    elif shape == "Ellipse":
        draw.ellipse([coords[0]-75, coords[1]-50, coords[0]+75, coords[1]+50], outline=color, width=3)
    return np.array(image_pil)

def join_images(image, direction):
    blank_image = np.zeros_like(image)
    if direction == "Horizontal":
        joined_image = np.hstack((image, blank_image))
    elif direction == "Vertical":
        joined_image = np.vstack((image, blank_image))
    elif direction == "Both":
        joined_image = np.hstack((image, blank_image))
        joined_image = np.vstack((joined_image, blank_image))
    return joined_image


