import streamlit as st

# Set up page title and layout
st.set_page_config(page_title="Tennis Game Tracking", layout="wide")

# Centered Page Title
st.markdown("<h1 style='text-align: center;'>Tennis Game Tracking</h1>", unsafe_allow_html=True)

# Create columns for layout
col1, col2 = st.columns([5, 1])  # Adjusts the width ratio of the main video area and sidebar

def display_video_area():
    """Display the main video area with a placeholder."""
    with col1:
        st.write("### Video")
        st.image("https://via.placeholder.com/600x300.png?text=Video+Display", width=800)  # Placeholder for video area

def display_controls():
    """Display the control buttons on the sidebar."""
    with col2:
        st.write("### Controls")
        st.write(" ")  # Empty space for alignment

        if st.button("Select Input File"):
            st.file_uploader("Choose a video file", type=["mp4", "avi", "mov"])
        
        if st.button("Preview Video"):
            st.write("Video preview function goes here.")
        
        if st.button("Show Output"):
            st.write("Output display function goes here.")
        
        if st.button("Download Output"):
            st.download_button("Download Processed Video", data="output.mp4", file_name="output.mp4", mime="video/mp4")
        # Display a progress bar at 40%
        progress = st.progress(0.4)

        if st.button("Process Video"):
            st.write("Video processing function goes here.")

# Display layout sections
display_video_area()
display_controls()
