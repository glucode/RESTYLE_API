import numpy as np
import cv2
import torch
import albumentations as albu
from iglovikov_helper_functions.utils.image_utils import load_rgb, pad, unpad
from iglovikov_helper_functions.dl.pytorch.utils import tensor_from_rgb_image
from cloths_segmentation.pre_trained_models import create_model
import os

model = create_model("Unet_2020-10-30")
model.eval() 

def segment_image(image_path, threshold=0.0):
    """
    Remove background.
    
    Parameters:
    - image_path: Path to the input image.
    - threshold: Threshold value to decide the mask from the prediction.
        
    Output:
    - Saves a file locally
    """
    


    image = load_rgb(image_path)

    transform = albu.Compose([albu.Normalize(p=1)], p=1)

    padded_image, pads = pad(image, factor=32, border=cv2.BORDER_CONSTANT)

    x = transform(image=padded_image)["image"]
    x = torch.unsqueeze(tensor_from_rgb_image(x), 0)

    with torch.no_grad():
        prediction = model(x)[0][0]

    # Use the threshold value passed to the function
    mask = (prediction > threshold).cpu().numpy().astype(np.uint8)
    mask = unpad(mask, pads)

    mask_rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)

    segmented_image = image * mask_rgb

    output_filename = os.path.basename(image_path)  # Get the original image file name
    output_path = os.path.join("uploads", f"{output_filename}_no_background.png")
    cv2.imwrite(output_path, cv2.cvtColor(segmented_image, cv2.COLOR_RGB2BGR))
    print(f"Image saved as {output_path}")

# Example usage with a threshold value:
# segment_image("Screenshot 2023-10-30 at 20.41.07.png")

