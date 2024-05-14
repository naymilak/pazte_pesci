import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
import albumentations as A

def load_image(image_path):

    coloured_image = cv2.imread(image_path)
    return coloured_image

def convolve2d(image, kernel):
    
    kernel = np.flipud(np.fliplr(kernel))
    output = np.zeros_like(image)

    image_padded = np.zeros((image.shape[0] + 2, image.shape[1] + 2, image.shape[2]))
    image_padded[1:-1, 1:-1, :] = image

    for c in range(image.shape[2]):
        for x in range(image.shape[1]):
            for y in range(image.shape[0]):
                output[y, x, c] = (kernel * image_padded[y: y+3, x: x+3, c]).sum()

    return output


transform = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.RandomBrightnessContrast(p=0.2),
    A.RandomRain(p=0.5)
])

save_dir = "augmented_images"
os.makedirs(save_dir, exist_ok=True)

input_image = load_image("../images/slika_01_03.png")

kernel = np.array([[0, 0, 0],
                   [0, 1, 0],
                   [0, 0, 0]])


output_image = convolve2d(input_image, kernel)

transformed = transform(image=output_image) 
transformed_image = transformed["image"]

plt.imsave(os.path.join(save_dir, "transformed_image.png"), transformed_image)

for i in range(5):
    transformed_image = transform(image=output_image)['image']
    plt.imsave(os.path.join(save_dir, f"transformed_image_{i+1}.png"), transformed_image)
