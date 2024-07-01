import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import torch
import numpy as np
import os

from models.common import DetectMultiBackend  # Pravilni modul iz YOLOv5
from utils.datasets import LoadImages
from utils.general import non_max_suppression, scale_coords
from utils.torch_utils import select_device

def letterbox(im, new_shape=(640, 640), color=(114, 114, 114), scaleup=True, stride=32):
    shape = im.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    # Scale ratio (new / old) 
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scaleup:  # only scale down, do not scale up (for better test mAP)
        r = min(r, 1.0)

    # Compute padding
    ratio = r, r  # width, height ratios
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
    dw /= 2  # divide padding into 2 sides
    dh /= 2

    if shape[::-1] != new_unpad:  # resize
        im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
    return im, ratio, (dw, dh)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Projektna naloga UI")

        self.root.geometry("1200x800")
        self.root.resizable(False, False)

        self.video_path = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.video_button = tk.Button(button_frame, text="Izberi videoposnetek", command=self.select_video)
        self.video_button.pack(side=tk.LEFT, padx=5)

        self.start_button = tk.Button(button_frame, text="Start", command=self.start_process)
        self.start_button.pack(side=tk.RIGHT, padx=5)

        self.canvas = tk.Canvas(self.root, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def select_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4")])
        if file_path:
            self.video_path.set(file_path)

    def start_process(self):
        if self.video_path.get():
            # Pot do shranjevanja modela
            model_path = r'model.pt'

            # Nalaganje modela prek YOLOv5 knjižnice
            try:
                device = select_device('')
                self.model = DetectMultiBackend(model_path, device=device)
                print("Model je uspešno naložen.")
            except Exception as e:
                print(f"Napaka pri nalaganju modela: {e}")
                import traceback
                traceback.print_exc()
                return

            self.process_video(self.video_path.get())
        else:
            messagebox.showwarning("Warning", "Izberite videoposnetek!")

    def process_video(self, video_path):
        cap = cv2.VideoCapture(video_path)

        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_rgb, _, _ = letterbox(frame_rgb)
                img = np.expand_dims(frame_rgb, axis=0)
                img = np.transpose(img, (0, 3, 1, 2))
                img = torch.from_numpy(img).float()

                device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                img = img.to(device)
                results = self.model(img)
                results.render()  # Render detections on image

                frame_with_objects = results.ims[0]  # Extract rendered image
                frame_with_objects = cv2.cvtColor(frame_with_objects, cv2.COLOR_RGB2BGR)

                self.show_frame(frame_with_objects)
                self.root.update()  # Osveži GUI
            else:
                break
        cap.release()

    def show_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_pil = Image.fromarray(frame)
        frame_tk = ImageTk.PhotoImage(frame_pil)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=frame_tk)
        self.canvas.image = frame_tk  # Ohranite referenco na sliko

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()