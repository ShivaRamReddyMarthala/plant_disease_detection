import cv2
import pandas as pd
from ultralytics import YOLO
import cvzone

class PlantDiseaseDetector:
    def __init__(self, model_path, class_list, confidence_threshold=0.5, iou_threshold=0.4, min_area_threshold=1000):
        self.model = YOLO(model_path)
        self.class_list = class_list
        self.confidence_threshold = confidence_threshold
        self.iou_threshold = iou_threshold
        self.min_area_threshold = min_area_threshold

    def detect_disease(self, image_path):
        image = cv2.imread(image_path)
        image = cv2.resize(image, (1020, 500))

        # Perform detection
        results = self.model.predict(image, conf=self.confidence_threshold, iou=self.iou_threshold)
        detections = results[0].boxes.data

        if detections is not None and len(detections) > 0:
            px = pd.DataFrame(detections).astype("float")
            for index, row in px.iterrows():
                x1, y1, x2, y2 = int(row[0]), int(row[1]), int(row[2]), int(row[3])
                confidence, class_id = row[4], int(row[5])
                class_name = self.class_list[class_id]

                # Calculate the area of the bounding box
                area = (x2 - x1) * (y2 - y1)

                # Filter by area size
                if area >= self.min_area_threshold:
                    color = (0, 255, 0)  # Green for valid detection
                    cv2.rectangle(image, (x1, y1), (x2, y2), color, 1)
                    cvzone.putTextRect(image, f'{class_name} {confidence:.2f}', (x1, y1), 1, 1)

            # Save the resulting image with a unique name
            output_path = image_path.replace('received', 'annotated')
            cv2.imwrite(output_path, image)
            return output_path

        else:
            print("No detections found in this image.")
            output_path = image_path.replace('received', 'annotated')
            cv2.imwrite(output_path, image)
            return output_path
            # return None
