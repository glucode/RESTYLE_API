import cv2
import numpy as np
import os
import pandas as pd

def extract_dominant_colors(image_path, k=4):
    """
    Extract dominant colors from the given image.
    """
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Image file not found at: {image_path}")

    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Failed to load the image from: {image_path}")
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pixels = image_rgb.reshape((-1, 3))
    pixels = np.float32(pixels)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    color_counts = np.bincount(labels.flatten())
    sorted_indices = np.argsort(color_counts)[-k:]
    dominant_colors = centers[sorted_indices]

    return dominant_colors

def extract_dominant_hsv(image_path):
    """
    Extract dominant HSV color from the given image.
    """
    dominant_colors_rgb = extract_dominant_colors(image_path, k=1)
    dominant_color_rgb = dominant_colors_rgb[0]
    dominant_color_hsv = cv2.cvtColor(np.uint8([[dominant_color_rgb]]), cv2.COLOR_RGB2HSV)[0][0]
    return dominant_color_hsv

# Load the dataset
df = pd.read_csv("external_Files/Dataset/Cleaned_Dataset.csv")

# Extract dominant HSV values and add them to the dataset
hues, saturations, values = [], [], []
image_folder = "external_Files/Dataset_images"

for product_id in df["Product ID"]:
    image_path = os.path.join(image_folder, f"{product_id}.png")
    try:
        hsv = extract_dominant_hsv(image_path)
        hues.append(hsv[0])
        saturations.append(hsv[1])
        values.append(hsv[2])
    except:
        hues.append(np.nan)
        saturations.append(np.nan)
        values.append(np.nan)

df["Hue"] = hues
df["Saturation"] = saturations
df["Value"] = values

# Save the updated dataset
df.to_csv("Updated_Dataset.csv", index=False)
