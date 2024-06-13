import streamlit as st
import cv2
import numpy as np
import requests
from datetime import datetime
from streamlit_webrtc import webrtc_streamer,VideoTransformerBase
from camera_input_live import camera_input_live
import av
import os

# Directory to save captured images
CAPTURE_DIR = "captured_images"
if not os.path.exists(CAPTURE_DIR):
    os.makedirs(CAPTURE_DIR)

st.title("Retinal Multi Disease Diagnosis App")

# Function to capture an image from the webcam
def capture_image(side, name):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret: 
        cap.release()
        filename = f"{CAPTURE_DIR}/{side}_Eye_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{name}.jpg"
        cv2.imwrite(filename, frame)
        return filename
    else:
        cap.release()
        st.error("Failed to capture image from webcam")
        return None

# UI to capture images
st.header("Capture Eye Images")
name = st.text_input("Enter Name")
right_eye_capture = st.button("Capture Right Eye")
left_eye_capture = st.button("Capture Left Eye")

if right_eye_capture:
    filename = capture_image("Right", name)
    if filename:
        st.success(f"Right eye image captured and saved as {filename}")

if left_eye_capture:
    filename = capture_image("Left", name)
    if filename:
        st.success(f"Left eye image captured and saved as {filename}")

# UI to display and crop captured images
st.header("Captured Images")
captured_files = [f for f in os.listdir(CAPTURE_DIR) if os.path.isfile(os.path.join(CAPTURE_DIR, f))]

if captured_files:
    selected_file = st.selectbox("Select a captured file", captured_files)
    if selected_file:
        file_path = os.path.join(CAPTURE_DIR, selected_file)
        image = cv2.imread(file_path)
        st.image(image, caption=selected_file, use_column_width=True)

        # Cropping UI
        st.subheader("Crop Image")
        x = st.slider("x", 0, image.shape[1], 0)
        y = st.slider("y", 0, image.shape[0], 0)
        width = st.slider("Width", 0, image.shape[1] - x, image.shape[1] - x)
        height = st.slider("Height", 0, image.shape[0] - y, image.shape[0] - y)
        
        if st.button("Crop Image"):
            cropped_image = image[y:y+height, x:x+width]
            cropped_filename = f"{CAPTURE_DIR}/cropped_{selected_file}"
            cv2.imwrite(cropped_filename, cropped_image)
            st.success(f"Image cropped and saved as {cropped_filename}")
            st.image(cropped_image, caption=cropped_filename, use_column_width=True)
else:
    st.info("No captured images found")
