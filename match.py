import streamlit as st
import cv2
import tempfile
import os

st.title("Tennis Game Tracking")

# Layout: create two columns
left_column, right_column = st.columns([3, 1])

# Video upload and display in the left column
with left_column:
    # Upload video
    uploaded_file = st.file_uploader("Select Input File", type=["mp4", "avi", "mov"])

    # Placeholder to preview video after upload
    if uploaded_file is not None:
        # Save the uploaded video to a temporary location
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        temp_file.write(uploaded_file.read())
        temp_file.close()

        # Preview uploaded video
        st.video(temp_file.name)
        st.session_state['temp_file_path'] = temp_file.name  # Store file path in session state

# Control buttons in the right column
with right_column:
    if uploaded_file is not None:
        # Progress display placeholder
        progress_text = st.empty()

        # Process Video
        if st.button("Process Video"):
            # Show processing status
            st.write("Processing the video...")

            # Path for processed video output
            output_file_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
            st.session_state['output_file_path'] = output_file_path

            # Video processing - keeping it in color
            cap = cv2.VideoCapture(temp_file.name)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for better compatibility with Streamlit
            out = cv2.VideoWriter(output_file_path, fourcc, cap.get(cv2.CAP_PROP_FPS), 
                                  (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))), 
                                  isColor=True)

            # Get total frames for progress tracking
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            processed_frames = 0

            # Process each frame and update progress
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                # Write the frame in original color
                out.write(frame)

                # Update progress
                processed_frames += 1
                progress_percentage = (processed_frames / total_frames) * 100
                progress_text.text(f"Processing: {int(progress_percentage)}%")

            cap.release()
            out.release()
            st.success("Video processed successfully!")

        # Show Output Video
        if 'output_file_path' in st.session_state and os.path.exists(st.session_state['output_file_path']) and st.button("Show Output"):
            st.video(st.session_state['output_file_path'])

        # Download Processed Video
        if 'output_file_path' in st.session_state and os.path.exists(st.session_state['output_file_path']):
            with open(st.session_state['output_file_path'], "rb") as f:
                processed_video = f.read()
            st.download_button(
                label="Download Output",
                data=processed_video,
                file_name="processed_video.mp4",
                mime="video/mp4"
            )

# Cleanup temporary files to prevent accumulation (optional)
# This will run only when the script finishes
if 'temp_file_path' in st.session_state and os.path.exists(st.session_state['temp_file_path']):
    os.remove(st.session_state['temp_file_path'])
if 'output_file_path' in st.session_state and os.path.exists(st.session_state['output_file_path']):
    os.remove(st.session_state['output_file_path'])
