from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import torch

class ClothingIdentifier():
    @staticmethod
    def identify(image_file):
        # Convert the FileStorage object to a PIL Image object
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
    
    
