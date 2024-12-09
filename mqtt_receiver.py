import paho.mqtt.client as mqtt
import base64
import numpy as np
import cv2
import uuid
import os
import requests
from plant_detector import PlantDiseaseDetector
import json

class MQTTImageReceiver:
    def __init__(self, broker_address, topic, plant_detector):
        # Initialize MQTT client
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.broker_address = broker_address
        self.topic = topic
        self.plant_detector = plant_detector
        self.save_directory = 'received_images/received/'  # Directory to save received images
        self.sensor_data_file = 'sensor_data.json' 
        os.makedirs(self.save_directory, exist_ok=True)  # Ensure the directory exists

        # Set up callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def generate_unique_filename(self):
        """Generate a unique filename using UUID."""
        return f'received_{uuid.uuid4()}.jpg'

    def save_sensor_data(self, sensor_data):
        """Save sensor data to a JSON file."""
        # Load existing data if the file exists
        if os.path.exists(self.sensor_data_file):
            with open(self.sensor_data_file, 'r') as file:
                data = json.load(file)
        else:
            data = []

        # Append the new sensor data
        data.append(sensor_data)

        # Save updated data back to the file
        with open(self.sensor_data_file, 'w') as file:
            json.dump(data, file, indent=4)


    def on_connect(self, client, userdata, flags, reason_code, properties=None):
        """Callback when the client connects to the MQTT broker."""
        print(f"Connected with result code {reason_code}")
        client.subscribe(self.topic)

    # def on_message(self, client, userdata, msg):
    #     """Callback when a message is received from the MQTT broker."""
    #     try:
    #         # Decode the image from the MQTT message payload
    #         print("Received")
    #         print(msg.payload)
    #         response = requests.get(msg.payload)
    #         response.raise_for_status()
    #         # image_data = base64.b64decode(msg.payload)
    #         # np_img = np.frombuffer(image_data, dtype=np.uint8)
    #         # img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    #         # Save the received image with a unique filename
    #         unique_filename = self.generate_unique_filename()
    #         full_image_path = os.path.join(self.save_directory, unique_filename)
    #         with open(full_image_path, 'wb') as file:
    #             file.write(response.content)
    #         # cv2.imwrite(full_image_path, img)
    #         print(f"Image received and saved as {full_image_path}")

    #         # Call the detection function
    #         annotated_image_path = self.plant_detector.detect_disease(full_image_path)
    #         if annotated_image_path:
    #             print(f"Annotated image saved at {annotated_image_path}")

    #     except Exception as e:
    #         print(f"Error processing message: {e}")

    def on_message(self, client, userdata, msg):
        """Callback when a message is received from the MQTT broker."""
        try:
            print("Received message from ESP32")
            message_content = msg.payload.decode()  # Decode the received message (URL or sensor data)

            # Check if the message is an image URL
            if message_content.startswith("http"):
                # It's a URL, download the image
                print(f"Downloading image from URL: {message_content}")
                response = requests.get(message_content)
                response.raise_for_status()

                # Generate a unique filename and save the downloaded image
                unique_filename = self.generate_unique_filename()
                full_image_path = os.path.join(self.save_directory, unique_filename)
                with open(full_image_path, 'wb') as file:
                    file.write(response.content)

                print(f"Image saved as {full_image_path}")

                # Call the plant disease detection function
                annotated_image_path = self.plant_detector.detect_disease(full_image_path)
                if annotated_image_path:
                    print(f"Annotated image saved at {annotated_image_path}")

            else:
                # Handle sensor data (assume it's a JSON-like string or sensor readings)
                try:
                    sensor_data = json.loads(message_content)  # Try to parse the message as JSON
                    print(f"Received sensor data: {sensor_data}")

                    # Save sensor data to a JSON file
                    self.save_sensor_data(sensor_data)
                    print(f"Sensor data saved to {self.sensor_data_file}")

                except json.JSONDecodeError:
                    # If message is not JSON, treat it as raw sensor data (e.g., temp, humidity)
                    print(f"Received raw sensor data: {message_content}")
                    sensor_data = {
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                        "data": message_content
                    }

                    # Save the raw sensor data to the JSON file
                    self.save_sensor_data(sensor_data)
                    print(f"Raw sensor data saved to {self.sensor_data_file}")

        except Exception as e:
            print(f"Error processing message: {e}")

    def start(self):
        """Start the MQTT client."""
        self.client.connect(self.broker_address, 1883, 60)
        self.client.loop_start()  # Non-blocking loop to handle messages
