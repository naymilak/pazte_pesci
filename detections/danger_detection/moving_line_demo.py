import numpy as np
import cv2
from shapely.geometry import Polygon
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Initialize danger zone points
danger_zone_points = np.array([
    [0, 560], [520, 530], [610, 500], [700, 500], [770, 530], [1280, 560]
], np.int32).reshape((-1, 1, 2))

# Function to update the image with the danger zone line
def update_image(canvas, img, points):
    img_copy = img.copy()
    cv2.polylines(img_copy, [points], isClosed=False, color=(0, 0, 255), thickness=2)
    img_pil = Image.fromarray(cv2.cvtColor(img_copy, cv2.COLOR_BGR2RGB))
    img_tk = ImageTk.PhotoImage(image=img_pil)
    canvas.img_tk = img_tk
    canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)

# Function to handle mouse events
def on_mouse_click(event, canvas, img, points):
    closest_idx = None
    min_dist = float('inf')
    for i, (x, y) in enumerate(points.reshape((-1, 2))):
        dist = (event.x - x)**2 + (event.y - y)**2
        if dist < min_dist:
            min_dist = dist
            closest_idx = i

    def on_drag(event):
        points[closest_idx] = [event.x, event.y]
        update_image(canvas, img, points)

    canvas.bind("<B1-Motion>", on_drag)

def main():
    root = tk.Tk()
    root.title("Danger Zone Editor")

    # Load image
    img_path = filedialog.askopenfilename()
    img = cv2.imread(img_path)
    img = cv2.resize(img, (1280, 720))

    canvas = tk.Canvas(root, width=1280, height=720)
    canvas.pack()

    update_image(canvas, img, danger_zone_points)

    canvas.bind("<Button-1>", lambda event: on_mouse_click(event, canvas, img, danger_zone_points))

    root.mainloop()

if __name__ == "__main__":
    main()
