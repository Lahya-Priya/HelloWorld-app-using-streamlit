import streamlit as st

# Set up page title and layout
st.set_page_config(page_title="Tennis Game Tracking", layout="wide")

# Page title
st.title("Tennis Game Tracking")

# Create columns for layout
col1, col2 = st.columns([5, 1])  # Adjusts the width ratio of the main video area and sidebar

# Main Video Display Area
with col1:
    st.write("### Video")
    st.image("https://via.placeholder.com/600x300.png?text=Video+Display", width=600)  # Placeholder for the video display area

# Sidebar for Controls
with col2:
    st.write(" ")  # Empty space for alignment
    st.write(" ")  # Empty space for alignment
    st.write(" ")  # Empty space for alignment

    if st.button("Select Input File"):
        st.file_uploader("Choose a video file", type=["mp4", "avi", "mov"])
        
    if st.button("Preview Video"):
        st.write("Video preview function goes here.")
        
    # Display a progress bar
    progress = st.progress(0.2)  # Example progress at 20%

    if st.button("Process Video"):
        st.write("Video processing function goes here.")
        
    if st.button("Show Output"):
        st.write("Output display function goes here.")

    if st.button("Download Output"):
        st.download_button("Download Processed Video", data="output.mp4", file_name="output.mp4", mime="video/mp4")
