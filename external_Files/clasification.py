import requests
from PIL import Image
from io import BytesIO
import torch
from transformers import AutoModelForImageClassification, AutoImageProcessor


class ClothingIdentifier():
    @staticmethod
    def identify(image_file):
        # Needs to be a image file from storage optionally look at down loading
        image = Image.open(image_file)

        preprocessor = AutoImageProcessor.from_pretrained("google/mobilenet_v2_1.0_224")
        model = AutoModelForImageClassification.from_pretrained("google/mobilenet_v2_1.0_224")

        inputs = preprocessor(images=image, return_tensors="pt")

        outputs = model(**inputs)
        logits = outputs.logits

        # Apply softmax to convert logits to probabilities
        probabilities = torch.nn.functional.softmax(logits, dim=-1)

        # Model predicts one of the 1000 ImageNet classes
        predicted_class_idx = logits.argmax(-1).item()
        predicted_confidence = probabilities[0, predicted_class_idx].item()

        return model.config.id2label[predicted_class_idx]
    
    


class URLClothingIdentifier():
    @staticmethod
    def identify_from_url(image_url):
        # Download image
        response = requests.get(image_url)
        if response.status_code != 200:
            raise ValueError("Failed to download the image from the provided URL")
        
        # Use BytesIO to create an in-memory binary stream of the image data
        image_data = BytesIO(response.content)
        image = Image.open(image_data)

        preprocessor = AutoImageProcessor.from_pretrained("google/mobilenet_v2_1.0_224")
        model = AutoModelForImageClassification.from_pretrained("google/mobilenet_v2_1.0_224")

        inputs = preprocessor(images=image, return_tensors="pt")

        outputs = model(**inputs)
        logits = outputs.logits

        # Apply softmax to convert logits to probabilities
        probabilities = torch.nn.functional.softmax(logits, dim=-1)

        # Model predicts one of the 1000 ImageNet classes
        predicted_class_idx = logits.argmax(-1).item()
        predicted_confidence = probabilities[0, predicted_class_idx].item()

        return model.config.id2label[predicted_class_idx]



# test_url = "https://galxboy.co.za/cdn/shop/products/image_5a6175ae-ac6f-4925-b349-74131c8be9d8.jpg?v=1694776300"  

# try:
#     result = URLClothingIdentifier.identify_from_url(test_url)
#     print(f"Predicted class for the image: {result}")
# except Exception as e:
#     print(f"An error occurred: {e}")