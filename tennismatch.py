import os
import gdown
import streamlit as st
import tempfile
import cv2
import numpy as np
import time
from ultralytics import YOLO

# Function to download model file with validation and retry logic
def download_file(url, file_path, retries=3, delay=2):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Retry download logic
    for attempt in range(retries):
        try:
            if not os.path.exists(file_path):
                gdown.download(url, file_path, quiet=True)  # Silent download
            # Verify the downloaded file is a PyTorch model and not an HTML page
            if os.path.getsize(file_path) < 1024 * 1024:  # Check for small file sizes
                os.remove(file_path)
                raise ValueError("Failed to download a valid model file. The file is too small to be a model.")
            
            with open(file_path, "rb") as f:
                first_bytes = f.read(10)
                if b'<' in first_bytes:  # HTML files often start with "<!DOCTYPE html>" or similar
                    os.remove(file_path)
                    raise ValueError("Downloaded file is not a valid model (it may be an HTML page).")
            return  # Successfully downloaded and verified model
        except (PermissionError, OSError) as e:
            if attempt < retries - 1:
                st.sidebar.warning(f"Attempt {attempt + 1} failed: {str(e)}. Retrying in {delay} seconds...")
                time.sleep(delay)  # Wait before retrying
            else:
                raise e  # Raise the error after final attempt

# Load YOLO model
@st.cache_resource
def load_model():
    model_path = "models/last.pt"
    model_url = "https://colab.research.google.com/drive/1zh47opd7AJ0aHX0-faPCZ64U42YCRIDq?usp=drive_link"  # Replace with actual Google Drive file ID
    
    # Download the model if not already present
    try:
        download_file(model_url, model_path)
        st.sidebar.text("Model downloaded successfully!")
    except Exception as e:
        st.sidebar.error(f"Error downloading model: {str(e)}")
        return None

    # Load YOLO model
    try:
        model = YOLO(model_path)
        st.sidebar.text("YOLO model loaded successfully!")
        return model
    except Exception as e:
        st.sidebar.error(f"Error loading YOLO model: {str(e)}")
        return None

# Process video function with preview
def process_video(input_path, output_path, preview=False):
    model = load_model()
    if model is None:
        st.sidebar.error("Model is not available. Cannot process video.")
        return False
    
    video = cv2.VideoCapture(input_path)
    if not video.isOpened():
        st.sidebar.error("Error: Could not open video file.")
        return False

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(video.get(cv2.CAP_PROP_FPS))
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    progress_bar = st.sidebar.progress(0)

    for i in range(frame_count):
        ret, frame = video.read()
        if not ret:
            st.sidebar.error(f"Error reading frame {i}.")
            break

        # Run YOLO inference
        results = model(frame)
        annotated_frame = results[0].plot()

        # Write annotated frame to output
        out.write(annotated_frame)

        # If preview is enabled, show the frame
        if preview:
            st.image(annotated_frame, channels="BGR", use_column_width=True)

        progress_bar.progress((i + 1) / frame_count)

    video.release()
    out.release()
    progress_bar.empty()
    return os.path.exists(output_path)

# Streamlit UI code
st.title("🎾 Tennis Game Tracking")
st.sidebar.title("Controls")
uploaded_file = st.sidebar.file_uploader("📂 Select Input Video File", type=["mp4", "avi", "mov"])

# Option to toggle video preview
preview_option = st.sidebar.checkbox("Show preview during processing", value=False)

if uploaded_file:
    # Save the uploaded file temporarily
    temp_input = tempfile.NamedTemporaryFile(delete=False)
    temp_input.write(uploaded_file.read())
    temp_input_path = temp_input.name
    temp_output_path = tempfile.mktemp(suffix=".mp4")

    if st.sidebar.button("Process Video"):
        st.sidebar.text("Processing Video...")
        success = process_video(temp_input_path, temp_output_path, preview=preview_option)
        
        if success:
            st.sidebar.text("Processing complete!")
            st.video(temp_output_path)

            # Provide a download link for the processed video
            with open(temp_output_path, "rb") as f:
                st.sidebar.download_button(
                    label="⬇️ Download Processed Video",
                    data=f.read(),
                    file_name="processed_video.mp4",
                    mime="video/mp4"
                )
        else:
            st.sidebar.error("Processing failed. Could not generate output video.")

    # Cleanup input file
    temp_input.close()
    os.remove(temp_input_path)
    if os.path.exists(temp_output_path):
        os.remove(temp_output_path)
else:
    st.info("Please upload a video file to start processing.")
