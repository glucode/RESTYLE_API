# Import necessary libraries
import numpy as np
import cv2
import torch
import albumentations as albu
from iglovikov_helper_functions.utils.image_utils import load_rgb, pad, unpad
from iglovikov_helper_functions.dl.pytorch.utils import tensor_from_rgb_image
from cloths_segmentation.pre_trained_models import create_model
import matplotlib.pyplot as plt

# Load the pre-trained model and set it to evaluation mode
model = create_model("Unet_2020-10-30")
model.eval()

# Load the image
image = load_rgb("IMG_1160 2.png")

# Define a normalization transformation
transform = albu.Compose([albu.Normalize(p=1)], p=1)

# Pad the image to make its dimensions divisible by 32
padded_image, pads = pad(image, factor=32, border=cv2.BORDER_CONSTANT)

# Convert the padded image to a tensor format suitable for the model
x = transform(image=padded_image)["image"]
x = torch.unsqueeze(tensor_from_rgb_image(x), 0)

# Get the segmentation mask from the model
with torch.no_grad():
    prediction = model(x)[0][0]

# Convert the prediction to a binary mask and remove padding
mask = (prediction > 0).cpu().numpy().astype(np.uint8)
mask = unpad(mask, pads)

mask_rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)

segmented_image = image * mask_rgb

plt.imshow(segmented_image)
plt.show()

# # Save the segmented image as a PNG
# output_path = f"{image}.png"
# cv2.imwrite(output_path, cv2.cvtColor(segmented_image, cv2.COLOR_RGB2BGR))
# print(f"Segmented image saved to {output_path}")

