import os
import sys
import json
import argparse
import numpy as np
from PIL import Image

import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

CLASSES = ['Arborio', 'Basmati', 'Ipsala', 'Jasmine', 'Karacadag']

class RicePredictor:
    """
    Rice Grain Image Classifier using MobileNetV2 CNN Model.
    """
    def __init__(self, model_path=None, class_indices_path=None):
        if model_path is None:
            if os.path.exists('model/rice_classifier.h5'):
                model_path = 'model/rice_classifier.h5'
            elif os.path.exists('rice_classifier.h5'):
                model_path = 'rice_classifier.h5'
            elif os.path.exists(r'C:\Users\visha\OneDrive - vit.ac.in\children_analysis\Rice_Image_Dataset\rice_classifier.h5'):
                model_path = r'C:\Users\visha\OneDrive - vit.ac.in\children_analysis\Rice_Image_Dataset\rice_classifier.h5'
            else:
                raise FileNotFoundError("Model file 'rice_classifier.h5' not found. Please run train.py first.")
                
        print(f"[INFO] Loading Rice Classifier CNN model from '{model_path}'...")
        self.model = load_model(model_path)
        
        if class_indices_path is None:
            if os.path.exists('model/class_indices.json'):
                class_indices_path = 'model/class_indices.json'
            elif os.path.exists('class_indices.json'):
                class_indices_path = 'class_indices.json'
            elif os.path.exists(r'C:\Users\visha\OneDrive - vit.ac.in\children_analysis\Rice_Image_Dataset\model\class_indices.json'):
                class_indices_path = r'C:\Users\visha\OneDrive - vit.ac.in\children_analysis\Rice_Image_Dataset\model\class_indices.json'
                
        if class_indices_path and os.path.exists(class_indices_path):
            with open(class_indices_path, 'r') as f:
                indices_map = json.load(f)
                self.index_to_class = {int(v) if isinstance(v, (int, str)) and str(v).isdigit() else v: k for k, v in indices_map.items()}
                # Ensure mapping key structure
                self.index_to_class = {v: k for k, v in indices_map.items()}
        else:
            self.index_to_class = {i: cls for i, cls in enumerate(CLASSES)}
            
    def predict_image(self, image_input):
        """
        Accepts PIL Image or file path string, resizes to 224x224, normalizes,
        and returns prediction dictionary with predicted class, confidence %, and all class probabilities.
        """
        if isinstance(image_input, str):
            if not os.path.exists(image_input):
                raise FileNotFoundError(f"Image path '{image_input}' does not exist.")
            img = Image.open(image_input).convert('RGB')
        elif isinstance(image_input, Image.Image):
            img = image_input.convert('RGB')
        else:
            raise ValueError("image_input must be a file path string or PIL Image object.")
            
        # Target size 224x224 as required for MobileNetV2
        img_resized = img.resize((224, 224))
        img_array = np.array(img_resized, dtype=np.float32)
        img_batch = np.expand_dims(img_array, axis=0)
        img_preprocessed = preprocess_input(img_batch)
        
        preds = self.model.predict(img_preprocessed, verbose=0)[0]
        
        max_idx = int(np.argmax(preds))
        predicted_class = self.index_to_class.get(max_idx, CLASSES[max_idx])
        confidence = float(preds[max_idx]) * 100.0
        
        probabilities = {}
        for idx, prob in enumerate(preds):
            cls_name = self.index_to_class.get(idx, CLASSES[idx] if idx < len(CLASSES) else f"Class_{idx}")
            probabilities[cls_name] = round(float(prob) * 100.0, 2)
            
        return {
            "predicted_class": predicted_class,
            "confidence": round(confidence, 2),
            "probabilities": probabilities
        }

# Global lazy-loaded predictor instance
_predictor = None

def get_predictor():
    global _predictor
    if _predictor is None:
        _predictor = RicePredictor()
    return _predictor

def predict_rice_image(image_path):
    predictor = get_predictor()
    return predictor.predict_image(image_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Classify a single rice grain image")
    parser.add_argument('--image', type=str, required=True, help='Path to rice image file')
    args = parser.parse_args()
    
    result = predict_rice_image(args.image)
    print("\n" + "="*45)
    print("RICE TYPE CLASSIFICATION RESULT")
    print("="*45)
    print(f"Predicted Class : {result['predicted_class']}")
    print(f"Confidence      : {result['confidence']:.2f}%")
    print("\nClass Probabilities:")
    for cls, prob in result['probabilities'].items():
        print(f" - {cls:<12}: {prob:.2f}%")
    print("="*45 + "\n")
