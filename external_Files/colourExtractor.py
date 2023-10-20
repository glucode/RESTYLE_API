import cv2
import numpy as np
import os
import webcolors

def rgb_to_color_name(rgb_color):
    try:
        closest_color = webcolors.rgb_to_name(rgb_color)
        return closest_color
    except ValueError:
        return "Unnamed Color"

def extract_dominant_colors(image_path, k=4):
    # Check if the file exists
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Image file not found at: {image_path}")

    # Load the image
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError(f"Failed to load the image from: {image_path}")

    # Convert the image from BGR to RGB (OpenCV loads images in BGR format)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Reshape the image to a 2D array of pixels
    pixels = image_rgb.reshape((-1, 3))

    # Convert pixel values to float32 for K-Means clustering
    pixels = np.float32(pixels)

    # Define criteria for K-Means clustering (stop when a specified accuracy is reached or after a maximum number of iterations)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)

    # Apply K-Means clustering to find dominant colors
    _, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Convert the centers of clusters to integer values
    centers = np.uint8(centers)

    # Sort the dominant colors by frequency
    color_counts = np.bincount(labels.flatten())
    sorted_indices = np.argsort(color_counts)[-k:]

    dominant_colors = centers[sorted_indices]

    # Convert RGB to color names with hex codes
    color_info = []
    for color in dominant_colors:
        hex_code = "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])
        color_name = rgb_to_color_name(color)
        color_info.append((hex_code, color_name))

    return color_info

# Example usage:
image_path = "uploads/102820308_C72_1.jpeg_no_background.png"  # Replace with the path to your image
dominant_colors = extract_dominant_colors(image_path, k=4)
print("Dominant Colors:")
for hex_code, color_name in dominant_colors:
    print(f"Hex: {hex_code}, Name: {color_name}")
