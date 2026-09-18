"""
Real image-based waste classification using TensorFlow/Keras.

This module provides actual computer vision classification for waste images.
It uses MobileNetV2 as a feature extractor with a custom classification head.

Since the reference garbage-classification-model repository does not provide
trained weights (garbage_classification_model_inception.h5), this implementation:

1. Uses a lightweight MobileNetV2 backbone for feasibility
2. Provides a clear architecture that can be trained when a dataset is available
3. Falls back gracefully when no trained model exists
4. Maps predictions to EcoSort categories correctly

Classes detected (when model is trained):
- cardboard → Dry/Recyclable
- glass → Dry/Recyclable  
- metal → Dry/Recyclable
- paper → Dry/Recyclable
- plastic → Dry/Recyclable
- trash → Other/Uncertain
"""

import os
from pathlib import Path
import numpy as np
from PIL import Image

# Optional TensorFlow import
try:
    import tensorflow as tf
    from tensorflow import keras
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False


# Waste classes that the model can detect
WASTE_CLASSES = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

# Map model classes to EcoSort categories
CLASS_TO_CATEGORY = {
    'cardboard': 'Dry/Recyclable',
    'glass': 'Dry/Recyclable',
    'metal': 'Dry/Recyclable',
    'paper': 'Dry/Recyclable',
    'plastic': 'Dry/Recyclable',
    'trash': 'Other/Uncertain',
}

# Image preprocessing parameters
IMG_HEIGHT = 224
IMG_WIDTH = 224


def get_model_path():
    """Return the expected path for the trained model weights."""
    return Path(__file__).parent.parent / "models" / "waste_classifier.h5"


def build_model(num_classes=6):
    """
    Build the waste classification model architecture.
    
    Uses MobileNetV2 as a feature extractor with custom classification head.
    This is a lightweight architecture suitable for deployment.
    """
    if not TF_AVAILABLE:
        return None
    
    base_model = keras.applications.MobileNetV2(
        input_shape=(IMG_HEIGHT, IMG_WIDTH, 3),
        include_top=False,
        weights='imagenet'  # Pre-trained on ImageNet for transfer learning
    )
    base_model.trainable = False  # Freeze the base model
    
    model = keras.Sequential([
        base_model,
        keras.layers.GlobalAveragePooling2D(),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(num_classes, activation='softmax')
    ])
    
    return model


def load_trained_model():
    """
    Load trained model weights if available.
    
    Returns:
        model: Loaded Keras model, or None if not available
        available: Boolean indicating if model is ready
    """
    if not TF_AVAILABLE:
        return None, False
    
    model_path = get_model_path()
    
    if not model_path.exists():
        # No trained model available yet
        return None, False
    
    try:
        model = keras.models.load_model(str(model_path))
        return model, True
    except Exception:
        # Model file exists but couldn't be loaded
        return None, False


def preprocess_image(image_file):
    """
    Preprocess uploaded image for classification.
    
    Args:
        image_file: File object or PIL Image
        
    Returns:
        numpy array: Preprocessed image ready for model
    """
    # Load image
    if hasattr(image_file, 'read'):
        # File-like object from Streamlit
        img = Image.open(image_file).convert('RGB')
    else:
        # PIL Image
        img = image_file.convert('RGB')
    
    # Resize to model input size
    img = img.resize((IMG_HEIGHT, IMG_WIDTH))
    
    # Convert to numpy array and normalize
    img_array = np.array(img) / 255.0
    
    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array


def classify_image(image_file):
    """
    Classify a waste image using the trained model.
    
    Args:
        image_file: Uploaded image file
        
    Returns:
        dict: Classification result with category, confidence, reason, detected_item
    """
    if not TF_AVAILABLE:
        return {
            'category': 'Other/Uncertain',
            'confidence': 'Low',
            'reason': 'TensorFlow is not installed. Image classification is unavailable.',
            'detected_item': 'Image upload (classification unavailable)',
        }
    
    model, available = load_trained_model()
    
    if not available or model is None:
        return {
            'category': 'Other/Uncertain',
            'confidence': 'Low',
            'reason': (
                'Trained model weights are not available. '
                'To enable image classification, train the model on a waste dataset '
                'and save weights to models/waste_classifier.h5'
            ),
            'detected_item': 'Image upload (model not trained)',
        }
    
    try:
        # Preprocess image
        img_array = preprocess_image(image_file)
        
        # Predict
        predictions = model.predict(img_array, verbose=0)
        predicted_idx = np.argmax(predictions[0])
        confidence_score = float(predictions[0][predicted_idx])
        
        # Get predicted class
        predicted_class = WASTE_CLASSES[predicted_idx]
        
        # Map to EcoSort category
        category = CLASS_TO_CATEGORY.get(predicted_class, 'Other/Uncertain')
        
        # Determine confidence level
        if confidence_score > 0.75:
            confidence = 'High'
        elif confidence_score > 0.50:
            confidence = 'Medium'
        else:
            confidence = 'Low'
        
        reason = (
            f'Image classification detected {predicted_class} '
            f'with {confidence_score:.1%} confidence.'
        )
        
        return {
            'category': category,
            'confidence': confidence,
            'reason': reason,
            'detected_item': f'{predicted_class} (from image)',
            'raw_confidence': confidence_score,
            'raw_class': predicted_class,
        }
        
    except Exception as e:
        return {
            'category': 'Other/Uncertain',
            'confidence': 'Low',
            'reason': f'Image classification failed: {str(e)}',
            'detected_item': 'Image upload (error)',
        }


def is_image_classification_available():
    """
    Check if image classification is available and ready to use.
    
    Returns:
        bool: True if TensorFlow is installed and model weights exist
    """
    if not TF_AVAILABLE:
        return False
    
    model_path = get_model_path()
    return model_path.exists()


def get_classification_status():
    """
    Get detailed status of image classification capability.
    
    Returns:
        dict: Status information
    """
    if not TF_AVAILABLE:
        return {
            'available': False,
            'reason': 'TensorFlow not installed',
            'action': 'Install TensorFlow: pip install tensorflow',
        }
    
    model_path = get_model_path()
    if not model_path.exists():
        return {
            'available': False,
            'reason': 'Model weights not found',
            'action': f'Train model and save to {model_path}',
        }
    
    return {
        'available': True,
        'reason': 'Ready',
        'model_path': str(model_path),
    }
