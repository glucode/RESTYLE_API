import numpy as np
import cv2
import torch
import albumentations as albu
from iglovikov_helper_functions.utils.image_utils import load_rgb, pad, unpad
from iglovikov_helper_functions.dl.pytorch.utils import tensor_from_rgb_image
from cloths_segmentation.pre_trained_models import create_model
import os 

def segment_image(image_path):
    """
    Remove background.
    
    Parameters:
    - Define a normalization transformation
    - Load the image from the FileStorage object
    - Pad the image to make its dimensions divisible by 32
    - Convert the padded image to a tensor format suitable for the model
    - Get the segmentation mask from the model
        
    Output:
    - Saves a file locally
    """
    model = create_model("Unet_2020-10-30")
    model.eval()

    image = load_rgb(image_path)

    transform = albu.Compose([albu.Normalize(p=1)], p=1)

    padded_image, pads = pad(image, factor=32, border=cv2.BORDER_CONSTANT)

    x = transform(image=padded_image)["image"]
    x = torch.unsqueeze(tensor_from_rgb_image(x), 0)

    with torch.no_grad():
        prediction = model(x)[0][0]


    mask = (prediction > 0).cpu().numpy().astype(np.uint8)
    mask = unpad(mask, pads)

    mask_rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)

    segmented_image = image * mask_rgb
 
    output_filename = os.path.basename(image_path)  # Get the original image file name
    output_path = os.path.join("uploads", f"{output_filename}_no_background.png")
    cv2.imwrite(output_path, cv2.cvtColor(segmented_image, cv2.COLOR_RGB2BGR))
    print(f"Image saved as {output_path}")

