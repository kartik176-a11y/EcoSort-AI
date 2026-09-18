"""
Image-based waste classification using InceptionV3.

This module integrates the garbage-classification approach from
https://github.com/vatsalparikh07/garbage-classification-model

NOTE: The source repository does NOT contain trained model weights.
This implementation uses InceptionV3 pre-trained on ImageNet with
intelligent waste category mapping based on detected objects.
"""

import io
import numpy as np
from PIL import Image

# Lazy imports for TensorFlow to avoid startup overhead
_tf = None
_inception_model = None
_imagenet_labels = None


# Mapping from ImageNet class names to waste categories
# Based on common waste items that InceptionV3 can recognize
IMAGENET_TO_WASTE_CATEGORY = {
    # Dry/Recyclable - Paper products
    "cardboard": "Dry/Recyclable",
    "carton": "Dry/Recyclable",
    "paper": "Dry/Recyclable",
    "newspaper": "Dry/Recyclable",
    "envelope": "Dry/Recyclable",
    "book": "Dry/Recyclable",
    "notebook": "Dry/Recyclable",
    
    # Dry/Recyclable - Plastic
    "plastic": "Dry/Recyclable",
    "bottle": "Dry/Recyclable",
    "water_bottle": "Dry/Recyclable",
    "pop_bottle": "Dry/Recyclable",
    "pill_bottle": "Dry/Recyclable",
    "container": "Dry/Recyclable",
    "bag": "Dry/Recyclable",
    "shopping_bag": "Dry/Recyclable",
    
    # Dry/Recyclable - Glass
    "glass": "Dry/Recyclable",
    "wine_bottle": "Dry/Recyclable",
    "beer_bottle": "Dry/Recyclable",
    "jar": "Dry/Recyclable",
    
    # Dry/Recyclable - Metal
    "can": "Dry/Recyclable",
    "beer_can": "Dry/Recyclable",
    "soda_can": "Dry/Recyclable",
    "tin": "Dry/Recyclable",
    "aluminum": "Dry/Recyclable",
    
    # Wet/Biodegradable
    "banana": "Wet/Biodegradable",
    "orange": "Wet/Biodegradable",
    "apple": "Wet/Biodegradable",
    "lemon": "Wet/Biodegradable",
    "fruit": "Wet/Biodegradable",
    "vegetable": "Wet/Biodegradable",
    "cucumber": "Wet/Biodegradable",
    "mushroom": "Wet/Biodegradable",
    "broccoli": "Wet/Biodegradable",
    "corn": "Wet/Biodegradable",
    
    # E-waste
    "cellular_telephone": "E-waste",
    "mobile_phone": "E-waste",
    "telephone": "E-waste",
    "laptop": "E-waste",
    "notebook_computer": "E-waste",
    "desktop_computer": "E-waste",
    "monitor": "E-waste",
    "screen": "E-waste",
    "mouse": "E-waste",
    "keyboard": "E-waste",
    "remote_control": "E-waste",
    "iPod": "E-waste",
    "joystick": "E-waste",
}


def _get_tensorflow():
    """Lazy-load TensorFlow to avoid import overhead."""
    global _tf
    if _tf is None:
        import tensorflow as tf
        _tf = tf
        # Suppress TensorFlow warnings
        import os
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    return _tf


def _get_inception_model():
    """Lazy-load InceptionV3 model with ImageNet weights."""
    global _inception_model
    if _inception_model is None:
        tf = _get_tensorflow()
        # Load InceptionV3 pre-trained on ImageNet
        # This automatically downloads weights from TensorFlow if not cached
        _inception_model = tf.keras.applications.InceptionV3(
            weights='imagenet',
            include_top=True,
            input_shape=(299, 299, 3)
        )
    return _inception_model


def _get_imagenet_labels():
    """Get ImageNet class labels."""
    global _imagenet_labels
    if _imagenet_labels is None:
        # ImageNet labels are built into TensorFlow/Keras
        # We'll decode predictions to get class names
        _imagenet_labels = True
    return _imagenet_labels


def preprocess_image(image_file):
    """
    Preprocess uploaded image for InceptionV3.
    
    Args:
        image_file: Streamlit UploadedFile object or PIL Image
        
    Returns:
        Preprocessed numpy array ready for model input
    """
    tf = _get_tensorflow()
    
    # Handle different input types
    if hasattr(image_file, 'read'):
        # Streamlit UploadedFile
        image_bytes = image_file.read()
        image_file.seek(0)  # Reset for potential re-use
        image = Image.open(io.BytesIO(image_bytes))
    elif isinstance(image_file, Image.Image):
        image = image_file
    else:
        raise ValueError("Unsupported image type")
    
    # Convert to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize to InceptionV3 input size (299x299)
    image = image.resize((299, 299), Image.Resampling.LANCZOS)
    
    # Convert to array and preprocess for InceptionV3
    img_array = np.array(image)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = tf.keras.applications.inception_v3.preprocess_input(img_array)
    
    return img_array


def map_imagenet_to_waste(decoded_predictions):
    """
    Map ImageNet predictions to waste categories.
    
    Args:
        decoded_predictions: List of (class_id, class_name, probability) tuples
        
    Returns:
        dict with predicted_class, confidence, category, explanation
    """
    # Try to map top predictions to waste categories
    for class_id, class_name, probability in decoded_predictions[:5]:
        class_name_lower = class_name.lower().replace('_', ' ')
        
        # Check direct mapping
        for keyword, category in IMAGENET_TO_WASTE_CATEGORY.items():
            if keyword in class_name_lower or class_name_lower in keyword:
                return {
                    'predicted_class': class_name.replace('_', ' ').title(),
                    'confidence': f"{probability * 100:.1f}%",
                    'category': category,
                    'explanation': f"Detected as {class_name.replace('_', ' ')} with {probability * 100:.1f}% confidence. Mapped to {category}.",
                    'imagenet_class': class_name,
                    'probability': float(probability)
                }
    
    # If no direct mapping found, use top prediction with "Other/Uncertain"
    top_class_id, top_class_name, top_probability = decoded_predictions[0]
    return {
        'predicted_class': top_class_name.replace('_', ' ').title(),
        'confidence': f"{top_probability * 100:.1f}%",
        'category': "Other/Uncertain",
        'explanation': f"Detected as {top_class_name.replace('_', ' ')} but could not map to a standard waste category. Please verify with text classification or local guidelines.",
        'imagenet_class': top_class_name,
        'probability': float(top_probability)
    }


def classify_waste_image(image_file):
    """
    Classify waste from uploaded image using InceptionV3.
    
    Args:
        image_file: Streamlit UploadedFile or PIL Image
        
    Returns:
        dict with classification results:
            - predicted_class: Human-readable class name
            - confidence: Confidence percentage
            - category: EcoSort waste category
            - explanation: Detailed explanation
            - success: Boolean indicating if classification succeeded
    """
    try:
        # Load model (lazy initialization)
        model = _get_inception_model()
        tf = _get_tensorflow()
        
        # Preprocess image
        img_array = preprocess_image(image_file)
        
        # Make prediction
        predictions = model.predict(img_array, verbose=0)
        
        # Decode predictions to human-readable labels
        decoded_predictions = tf.keras.applications.inception_v3.decode_predictions(
            predictions, top=5
        )[0]
        
        # Map to waste categories
        result = map_imagenet_to_waste(decoded_predictions)
        result['success'] = True
        result['model'] = 'InceptionV3-ImageNet'
        
        # Add all top-5 predictions for transparency
        result['top_predictions'] = [
            {
                'class': name.replace('_', ' ').title(),
                'confidence': f"{prob * 100:.1f}%"
            }
            for _, name, prob in decoded_predictions
        ]
        
        return result
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'predicted_class': 'Error',
            'confidence': 'N/A',
            'category': 'Other/Uncertain',
            'explanation': f"Image classification failed: {str(e)}. Please use text classification instead.",
            'model': 'InceptionV3-ImageNet'
        }


def is_available():
    """Check if image classification is available (TensorFlow installed)."""
    try:
        _get_tensorflow()
        return True
    except ImportError:
        return False
