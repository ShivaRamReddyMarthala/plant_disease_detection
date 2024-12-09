import streamlit as st
from PIL import Image
import os

class StreamlitDashboard:
    def __init__(self, image_directory):
        self.image_directory = image_directory

    def get_latest_image(self):
        # List all annotated images and get the latest one
        images = [img for img in os.listdir(self.image_directory) if img.startswith('annotated_')]
        if images:
            latest_image = max(images, key=lambda x: os.path.getctime(os.path.join(self.image_directory, x)))
            return os.path.join(self.image_directory, latest_image)
        return None

    def display(self):
        st.title("Plant Disease Detection Dashboard")
        st.header("Detected Plant Diseases with Bounding Boxes")

        latest_image_path = self.get_latest_image()
        if latest_image_path:
            image = Image.open(latest_image_path)
            st.image(image, caption=f'Annotated Image: {os.path.basename(latest_image_path)}', use_column_width=True)
        else:
            st.write("No image to display.")
