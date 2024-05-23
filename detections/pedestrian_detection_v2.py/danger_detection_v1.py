import numpy as np
import cv2
from shapely.geometry import Polygon, box
import matplotlib.pyplot as plt

# Define the danger zone path points
danger_zone_points = np.array([
    [0, 560], [520, 530], [610, 500], [700, 500], [770, 530], [1280, 560]
], np.int32).reshape((-1, 1, 2))

# Convert danger zone points to Shapely polygon
danger_zone_polygon = Polygon(danger_zone_points.reshape((-1, 2)))

def is_pedestrian_in_danger_zone(detections, danger_zone_polygon):
    for (x1, y1, x2, y2) in detections:
        pedestrian_box = box(x1, y1, x2, y2)  # Create a Shapely box object for the pedestrian
        if danger_zone_polygon.intersects(pedestrian_box):
            return True
    return False

"""
# Check if any detection intersects with the danger zone
if is_pedestrian_in_danger_zone(detections, danger_zone_polygon):
    print("Watch out! Pedestrian in danger zone.")
"""
    
def danger_detection(det):
    det = det
    return is_pedestrian_in_danger_zone(det, danger_zone_polygon)
