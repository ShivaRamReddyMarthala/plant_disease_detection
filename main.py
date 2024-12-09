from plant_detector import PlantDiseaseDetector
from mqtt_receiver import MQTTImageReceiver
import streamlit as st
import json
import os
from glob import glob

def load_latest_sensor_data(json_file):
    """Load the latest two sensor data entries from the JSON file."""
    if os.path.exists(json_file):
        with open(json_file, 'r') as file:
            data = json.load(file)
            if data:
                latest_data = data[-2:]  # Get the last two entries
                combined_data = {}
                for entry in latest_data:
                    combined_data.update(entry)  # Merge the last two entries
                return combined_data
    return None

def get_last_n_images(image_directory, n=5):
    """Get the last 'n' images from the annotated images directory."""
    image_list = glob(os.path.join(image_directory, "*.jpg"))
    if image_list:
        sorted_images = sorted(image_list, key=os.path.getctime, reverse=True)  # Sort by creation time
        return sorted_images[:n]
    return []

if __name__ == '__main__':
    # Define class labels for the plant disease detector
    class_list = ['Black Rot', 'Cedar Apple Rust', 'Apple Scab']

    # Initialize the plant disease detector
    detector = PlantDiseaseDetector(model_path='models/best 2.pt', class_list=class_list)

    # Start the MQTT receiver
    receiver = MQTTImageReceiver(
        broker_address="test.mosquitto.org",
        topic="plant/disease/data",
        plant_detector=detector
    )
    receiver.start()

    # Streamlit dashboard interface
    st.title("Plant Disease Detection Dashboard")

    # Display the latest sensor data
    st.subheader("Latest Sensor Data")
    latest_sensor_data = load_latest_sensor_data('sensor_data.json')
    if latest_sensor_data:
        st.json(latest_sensor_data)
    else:
        st.write("No sensor data available yet.")

    # Button to refresh images
    if st.button('Refresh Images'):
        st.write("Images refreshed!")

    # Display the last 5 annotated images
    st.subheader("Last 5 Annotated Images")
    image_directory = 'annotated_images/annotated/'
    last_images = get_last_n_images(image_directory, n=5)

    if last_images:
        for image_path in last_images:
            st.image(image_path, caption=f"Annotated Image: {os.path.basename(image_path)}", use_column_width=True)
    else:
        st.write("No annotated images available yet.")
