# Image Classification Integration

## Overview

This document describes the integration of real waste image classification into EcoSort AI, based on the approach from [vatsalparikh07/garbage-classification-model](https://github.com/vatsalparikh07/garbage-classification-model).

## Source Repository Analysis

### What We Found

The source repository (`vatsalparikh07/garbage-classification-model`) contains:
- ✓ `app.py` - Streamlit application expecting a trained model
- ✓ `wastemanagement.ipynb` - Training notebook using InceptionV3
- ✓ `README.md` - Documentation of the approach
- **✗ No trained model weights file** (`garbage_classification_model_inception.h5`)

### Critical Finding

**The source repository does NOT contain the trained model weights file.**

The `app.py` file tries to load `garbage_classification_model_inception.h5`, but this file does not exist in the repository. The repository only provides the training code and application structure.

## Our Solution

Since no trained model weights were available, we implemented a practical solution that:

1. **Uses InceptionV3 with ImageNet pre-trained weights**
   - TensorFlow/Keras automatically downloads these weights (154 MB)
   - No need to commit large model files to GitHub
   
2. **Implements intelligent category mapping**
   - Maps ImageNet object classes to EcoSort waste categories
   - Example: "plastic_bottle" → Dry/Recyclable
   - Example: "banana" → Wet/Biodegradable
   - Example: "laptop" → E-waste

3. **Graceful degradation**
   - Works without TensorFlow (text classification only)
   - Shows clear status in UI about capabilities

## Implementation

### Files Created

1. **`src/image_classifier.py`**
   - Core image classification module
   - InceptionV3 model loading (lazy initialization)
   - Image preprocessing (resize to 299×299, normalize)
   - ImageNet → EcoSort category mapping
   - Top-5 predictions for transparency

2. **`src/agents.py` (updated)**
   - Integrated image classification into workflow
   - Priority: Image classification > Text classification
   - Combines both when available
   - Falls back gracefully when TensorFlow unavailable

3. **`app.py` (updated)**
   - Enhanced UI for image upload
   - Shows classification method (image vs text)
   - Displays top-5 predictions for transparency
   - System capabilities indicator in sidebar

4. **`requirements.txt` (updated)**
   - Added `tensorflow>=2.13.0`
   - Added `pillow>=10.0.0`
   - Added `numpy>=1.24.0`

## Waste Category Mapping

### ImageNet Classes Mapped to EcoSort Categories

#### Dry/Recyclable
- Paper: cardboard, carton, paper, newspaper, envelope, book, notebook
- Plastic: plastic, bottle, water_bottle, pop_bottle, pill_bottle, container, bag
- Glass: glass, wine_bottle, beer_bottle, jar
- Metal: can, beer_can, soda_can, tin, aluminum

#### Wet/Biodegradable
- Fruits: banana, orange, apple, lemon, fruit
- Vegetables: vegetable, cucumber, mushroom, broccoli, corn

#### E-waste
- Electronics: cellular_telephone, mobile_phone, laptop, notebook_computer, desktop_computer
- Peripherals: monitor, screen, mouse, keyboard, remote_control
- Other: iPod, joystick

#### Other/Uncertain
- Any ImageNet class not in the above mappings

## Workflow

```
UPLOAD IMAGE
      ↓
IMAGE PREPROCESSING
  - Resize to 299×299
  - Convert to RGB
  - Normalize for InceptionV3
      ↓
INCEPTION V3 PREDICTION
  - Top-5 ImageNet classes
  - Confidence scores
      ↓
CATEGORY MAPPING
  - Map to EcoSort categories
  - Fall back to "Other/Uncertain"
      ↓
RAG RETRIEVAL
  - Use detected item name
  - Retrieve disposal guidance
      ↓
LLM GENERATION
  - Granite or fallback
  - Grounded recommendation
      ↓
DISPLAY RESULTS
  - Category, confidence, method
  - Top predictions
  - Disposal guidance
  - Responsible AI disclaimer
```

## Installation

### Full Installation (with image classification)

```bash
git clone https://github.com/kartik176-a11y/EcoSort-AI.git
cd EcoSort-AI
git checkout feature/waste-image-classification
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**Note:** TensorFlow download is ~500 MB. First-time model initialization downloads InceptionV3 weights (~154 MB).

### Minimal Installation (text-only)

```bash
pip install streamlit requests pypdf
```

The app will work in text-classification mode and show a message about installing TensorFlow.

## Usage

### With Image Classification

1. Run the app:
   ```bash
   streamlit run app.py
   ```

2. Upload an image of waste (JPG, PNG, JPEG, WEBP)

3. Optionally enter a text description

4. Click "Analyze Waste"

5. View results:
   - Classification method (Image/Text)
   - Detected item
   - Waste category
   - Confidence
   - Top-5 predictions
   - Disposal recommendation
   - RAG-retrieved guidance

### Text-Only Mode

If TensorFlow is not installed:
- Image uploads show preview only
- Text classification is used
- UI shows installation instructions for image classification

## Model Performance

### Strengths

- **Good at common recyclables:**
  - Plastic bottles, cans, glass bottles
  - Paper products, cardboard
  - Metal containers

- **Good at fresh produce:**
  - Fruits and vegetables (for Wet/Biodegradable)

- **Good at electronics:**
  - Phones, laptops, monitors (for E-waste)

### Limitations

- **Not trained specifically on waste:**
  - InceptionV3 was trained on general objects (ImageNet)
  - May misclassify mixed/dirty waste
  - May not recognize regional waste items

- **Cannot detect:**
  - Hazardous waste (batteries, chemicals) unless object shape matches
  - Contamination or multi-material items
  - Condition (clean vs dirty, recyclable vs not)

- **Requires clear images:**
  - Good lighting
  - Single object focus
  - Clear background preferred

### Accuracy Notes

This is **NOT** the same as a model trained specifically on waste datasets. Performance depends on:
- Image quality
- Object visibility
- Similarity to ImageNet training data

**Always verify with text classification and local guidelines for critical decisions.**

## Comparison with Source Repository

| Aspect | Source Repo | Our Implementation |
|--------|-------------|-------------------|
| Model file | Missing (expected but not present) | Not needed (uses TensorFlow weights) |
| Model weights | Not available | InceptionV3-ImageNet (auto-download) |
| Training data | Not available | Pre-trained on ImageNet |
| Waste categories | 6 (Cardboard, Trash, Plastic, Metal, Glass, Paper) | 5 (Wet, Dry, Hazardous, E-waste, Other) |
| Integration | Standalone app | Integrated with RAG + LLM pipeline |
| Deployment | Requires trained model | Works out-of-the-box with TensorFlow |
| GitHub size | 788 KB (notebook only) | Minimal (weights downloaded on demand) |

## Future Improvements

### Short-term
1. Add support for multiple images
2. Implement image quality checks
3. Add batch processing

### Medium-term
1. Fine-tune InceptionV3 on actual waste datasets
2. Add data augmentation for training
3. Collect user feedback for model improvement

### Long-term
1. Train custom model on Indian waste categories
2. Add region-specific waste recognition
3. Integrate with GVMC (Vizag) waste management data
4. Support multilingual UI (Telugu, Hindi, English)

## Testing

### Test Cases

1. **Plastic bottle** (image)
   - Expected: Dry/Recyclable
   - Method: Image classification

2. **Banana** (image)
   - Expected: Wet/Biodegradable
   - Method: Image classification

3. **Mobile phone** (image)
   - Expected: E-waste
   - Method: Image classification

4. **Unknown object** (image)
   - Expected: Other/Uncertain
   - Method: Image classification with fallback

5. **"plastic bottle"** (text only)
   - Expected: Dry/Recyclable
   - Method: Text classification

6. **No TensorFlow installed**
   - Expected: Text classification only
   - UI: Shows installation message

## Troubleshooting

### TensorFlow Installation Issues

**Problem:** Large download size (~500 MB)
- **Solution:** Use `tensorflow-cpu` for smaller size (no GPU support)
  ```bash
  pip install tensorflow-cpu>=2.13.0
  ```

**Problem:** Import errors
- **Solution:** Ensure Python 3.8-3.11 (TensorFlow compatibility)

**Problem:** First run is slow
- **Solution:** InceptionV3 weights are being downloaded (one-time, ~154 MB)

### Image Classification Not Working

**Problem:** "Image classification unavailable" message
- **Solution:** Install TensorFlow: `pip install tensorflow`

**Problem:** Low confidence predictions
- **Solution:** 
  - Use clearer, well-lit images
  - Focus on single object
  - Try text classification as backup

**Problem:** Wrong category detected
- **Solution:**
  - Verify with text classification
  - Check top-5 predictions
  - Use text description as override

## Responsible AI

- Image classification is a **helpful tool, not a replacement** for human judgment
- Always verify critical waste disposal decisions (hazardous, e-waste) with local authorities
- Model may misclassify items not in ImageNet or waste-specific training data
- User privacy: Images are processed locally and not stored by default
- Transparent predictions: Top-5 predictions shown for user verification

## Credits

- **Source inspiration:** [vatsalparikh07/garbage-classification-model](https://github.com/vatsalparikh07/garbage-classification-model)
- **Model:** InceptionV3 (Google) via TensorFlow/Keras
- **Integration:** Developed for EcoSort AI by V.Karthik
- **Purpose:** 1M1B AI for Sustainability Virtual Internship

## License

This integration follows the same license as EcoSort AI (MIT License).
TensorFlow and InceptionV3 weights follow their respective licenses (Apache 2.0).
