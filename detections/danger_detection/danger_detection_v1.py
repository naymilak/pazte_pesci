import numpy as np
import cv2
from shapely.geometry import Polygon, box
import matplotlib.pyplot as plt

# Define the danger zone path points
danger_zone_points = np.array([
    [0, 560], [520, 530], [610, 500], [700, 500], [770, 530], [1280, 560]
], np.int32).reshape((-1, 1, 2))

# Create the danger zone polygon using OpenCV and add pedestrian bounding boxes
def create_danger_zone_image(background_img, danger_zone_points, detections):
    img = background_img.copy()  # Use the provided background image
    img = cv2.resize(img, (1280, 720))  # Resize background image to 1280x720
    # Draw the danger zone path
    cv2.polylines(img, [danger_zone_points], isClosed=False, color=(0, 0, 255), thickness=2)
    
    # Draw the bounding boxes for detected pedestrians
    for (x1, y1, x2, y2) in detections:
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
    return img

# Example pedestrian detections (x1, y1, x2, y2) - normally obtained from YOLOv5
detections = [(953, 412, 1041, 581)]  # Example detections

# Load the background image and resize it to 1280x720
frame = cv2.imread("slika_02_27.png")  # Change "background_image.jpg" to your image path
frame = cv2.resize(frame, (1280, 720))

# Display the danger zone and detections for visualization using Matplotlib
danger_zone_img = create_danger_zone_image(frame, danger_zone_points, detections)

plt.imshow(cv2.cvtColor(danger_zone_img, cv2.COLOR_BGR2RGB))
plt.title('Danger Zone with Detections')
plt.show()

# Convert danger zone points to Shapely polygon
danger_zone_polygon = Polygon(danger_zone_points.reshape((-1, 2)))

def is_pedestrian_in_danger_zone(detections, danger_zone_polygon):
    for (x1, y1, x2, y2) in detections:
        pedestrian_box = box(x1, y1, x2, y2)  # Create a Shapely box object for the pedestrian
        if danger_zone_polygon.intersects(pedestrian_box):
            return True
    return False

# Check if any detection intersects with the danger zone
if is_pedestrian_in_danger_zone(detections, danger_zone_polygon):
    print("Watch out! Pedestrian in danger zone.")
    
def danger_detection(detections):
    return is_pedestrian_in_danger_zone(detections, danger_zone_polygon)
