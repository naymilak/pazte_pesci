import numpy as np
import cv2
from shapely.geometry import Polygon, box
import matplotlib.pyplot as plt

# svg crta
danger_zone_points = np.array([
    [0, 560], [520, 530], [610, 500], [700, 500], [770, 530], [1280, 560]
], np.int32).reshape((-1, 1, 2))

# ustvarimo mejo nevarnosti in izrisemo + izris detekcije
def create_danger_zone_image(background_img, danger_zone_points, detections):
    img = background_img.copy()
    img = cv2.resize(img, (1280, 720))
    # meja nevarnosti
    cv2.polylines(img, [danger_zone_points], isClosed=False, color=(0, 0, 255), thickness=2)
    
    # izris boxov za pesce
    for (x1, y1, x2, y2) in detections:
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
    return img

# testni primer detekcije
detections = [(953, 412, 1041, 581)]

frame = cv2.imread("slika_02_27.png")  # vnos testne slike
frame = cv2.resize(frame, (1280, 720))

# izris meje nevarnosti
danger_zone_img = create_danger_zone_image(frame, danger_zone_points, detections)

plt.imshow(cv2.cvtColor(danger_zone_img, cv2.COLOR_BGR2RGB))
plt.title('Detekcija nevarnosti')
plt.show()

# spremenimo mejo v polygon
danger_zone_polygon = Polygon(danger_zone_points.reshape((-1, 2)))

# FUNKCIJA ZA PREVERJANJE NEVARNOSTI
def is_pedestrian_in_danger_zone(detections, danger_zone_polygon):
    for (x1, y1, x2, y2) in detections:
        pedestrian_box = box(x1, y1, x2, y2)  # ustvari box
        if danger_zone_polygon.intersects(pedestrian_box):
            return True
    return False

# preverimo nevarnosti za testni primer
if is_pedestrian_in_danger_zone(detections, danger_zone_polygon):
    print("PAZI PESEC!")
    
# funkcija za skripto pedestrian_detection_v1.py
def danger_detection(detections):
    return is_pedestrian_in_danger_zone(detections, danger_zone_polygon)