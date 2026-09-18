# Models Directory

This directory stores trained machine learning model weights for image classification.

## Expected Files

### waste_classifier.h5
- **Purpose**: Trained MobileNetV2-based waste classification model
- **Size**: ~10-20 MB (not committed to git)
- **Classes**: cardboard, glass, metal, paper, plastic, trash
- **Input**: 224x224 RGB images
- **Output**: 6-class softmax probabilities

## Current Status

**Model weights are NOT included in this repository.**

The image classification module (`src/image_classifier.py`) is ready but requires trained weights to function.

## How to Enable Image Classification

### Option 1: Train Your Own Model

1. Collect a waste classification dataset (e.g., from Kaggle or custom collection)
2. Use the model architecture defined in `src/image_classifier.py`
3. Train the model on your dataset
4. Save the trained weights to `models/waste_classifier.h5`

Example training code:

```python
from src.image_classifier import build_model
import tensorflow as tf

# Prepare your dataset (not shown here)
train_dataset = ...  # Your training data
val_dataset = ...    # Your validation data

# Build model
model = build_model(num_classes=6)

# Compile
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Train
model.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=10
)

# Save
model.save('models/waste_classifier.h5')
```

### Option 2: Use Pre-trained Weights

If you have access to pre-trained weights from another waste classification project:

1. Ensure the model has the same architecture (MobileNetV2 base, 6 classes)
2. Ensure the classes match: cardboard, glass, metal, paper, plastic, trash
3. Copy the `.h5` file to this directory
4. Restart the Streamlit app

### Option 3: Use Reference Model (Advanced)

The reference repository [vatsalparikh07/garbage-classification-model](https://github.com/vatsalparikh07/garbage-classification-model) mentions a model file `garbage_classification_model_inception.h5` but does not provide it in the repository.

If you can obtain compatible trained weights, you may need to:
- Convert InceptionV3-based weights to MobileNetV2 format, OR
- Modify `src/image_classifier.py` to use InceptionV3 architecture instead

## Datasets

Public waste classification datasets:

- **TrashNet** (Kaggle)
- **Waste Classification Data** (Kaggle)
- **TACO Dataset** (Trash Annotations in Context)

Search for "waste classification dataset" on Kaggle or similar platforms.

## Without Trained Weights

The app will continue to work using:
- **Text-based classification** (fully functional)
- **RAG retrieval** (fully functional)
- **IBM Granite / Local fallback** (fully functional)

Image uploads will show a clear message that the model is not trained yet.

## Notes

- Model files (`.h5`, `.hdf5`, `.pb`, `.pth`, `.onnx`) are excluded from git via `.gitignore`
- Do NOT commit large model files to GitHub
- For deployment, use model hosting services or artifact storage
