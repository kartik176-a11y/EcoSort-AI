# Quick Start Guide

Get EcoSort AI running in 5 minutes!

## Prerequisites

- Python 3.8 or higher installed
- Git installed
- Internet connection (for installing dependencies)

---

## Option 1: Quick Start (Without Image Classification)

This is the fastest way to get started. Image uploads will work but fall back to text classification.

### 1. Clone the Repository

```bash
git clone https://github.com/kartik176-a11y/EcoSort-AI.git
cd EcoSort-AI
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

**Activate it:**

Linux/macOS:
```bash
source .venv/bin/activate
```

Windows:
```cmd
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
streamlit run app.py
```

### 5. Open in Browser

Open http://localhost:8501 in your browser.

### 6. Try It Out

**Test with text input:**
- Enter: "banana peel"
- Click: Analyze Waste
- See: Wet/Biodegradable category with disposal guidance

**More examples:**
- plastic bottle → Dry/Recyclable
- used battery → Hazardous/Special Waste
- old mobile phone → E-Waste

---

## Option 2: Full Install (With Image Classification)

Enable real computer vision classification of waste images.

### 1-3. Same as Option 1

Follow steps 1-3 from Option 1 above.

### 4. Install TensorFlow

**For CPU-only** (recommended, smaller download):
```bash
pip install tensorflow-cpu
```

**OR for GPU support** (larger, needs CUDA):
```bash
pip install tensorflow
```

### 5. Get or Train Model Weights

**Option A: Train your own model**

See `models/README.md` for detailed training instructions.

**Option B: Use pre-trained weights** (if available)

If you have compatible weights:
```bash
# Create models directory if needed
mkdir -p models

# Copy your trained model
cp path/to/waste_classifier.h5 models/
```

### 6. Run the App

```bash
streamlit run app.py
```

### 7. Test Image Classification

- Upload an image of waste (cardboard, plastic, glass, etc.)
- See real computer vision classification results

---

## Option 3: With IBM Granite (Optional)

Add IBM Granite LLM for enhanced recommendations.

### 1-4. Complete Option 1 or 2 first

### 5. Configure IBM Granite

Create `.env` file:
```bash
cp .env.example .env
```

Edit `.env` and add your credentials:
```env
IBM_GRANITE_ENDPOINT=https://your-endpoint/v1/chat/completions
IBM_GRANITE_MODEL=ibm-granite
IBM_API_KEY=your_api_key_here
```

### 6. Run the App

```bash
streamlit run app.py
```

The app will now use IBM Granite for generating recommendations while still grounding them in retrieved evidence.

---

## Verify Installation

### Run Tests

```bash
python run_tests.py
```

**Expected output:**
```
=== Running Classifier Tests ===
✓ Text normalization works
✓ Wet waste classification works
✓ Dry recyclable classification works
...
=== ALL TESTS PASSED ===
```

### Check System Status

When the app is running, look at the sidebar:

**Green checkmarks mean:**
- ✓ IBM Granite configured (if .env set)
- ✓ Image classification ready (if TensorFlow + model)

**Info/Warning messages mean:**
- ℹ Local fallback mode (IBM not configured - this is fine!)
- ⚠ Image: TensorFlow not installed (expected if you chose Option 1)
- ⚠ Image: Model weights not found (expected until you train a model)

---

## Troubleshooting

### "streamlit: command not found"

```bash
# Make sure virtual environment is activated
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Try reinstalling
pip install --upgrade streamlit
```

### "No module named 'src'"

Make sure you're running from the project root directory:
```bash
cd EcoSort-AI  # Navigate to project root
streamlit run app.py
```

### TensorFlow Installation Issues

**macOS Apple Silicon (M1/M2)**:
```bash
pip install tensorflow-macos
```

**Windows without AVX**:
```bash
pip install tensorflow-cpu
```

**Linux**:
```bash
pip install tensorflow-cpu  # CPU-only
# OR
pip install tensorflow      # With GPU support
```

### Port Already in Use

If port 8501 is busy:
```bash
streamlit run app.py --server.port 8502
```

### Image Upload Not Working

This is expected behavior if:
1. TensorFlow not installed → Install it (Option 2)
2. Model weights missing → Train model (see `models/README.md`)

The app will clearly tell you what's missing. Text classification always works!

---

## Next Steps

### Learn More

- Read `README.md` for complete documentation
- Check `models/README.md` to train image classifier
- Review `data/` folder for knowledge base documents
- Explore `src/` for code organization

### Customize

- **Add Knowledge**: Edit files in `data/` folder
- **Change Categories**: Modify `src/classifier.py`
- **UI Tweaks**: Edit `app.py`
- **Add Languages**: Contribute translations!

### Deploy

For production deployment, consider:
- Streamlit Cloud (free tier available)
- Heroku
- AWS/GCP/Azure
- Docker container

---

## Need Help?

- **GitHub Issues**: https://github.com/kartik176-a11y/EcoSort-AI/issues
- **Documentation**: See `README.md`
- **Model Training**: See `models/README.md`

---

## What Works Without Setup

Even with minimal installation (Option 1), you get:

✅ Full text-based classification
✅ RAG retrieval from knowledge base  
✅ Local fallback recommendations
✅ All 5 waste categories
✅ Source attribution
✅ Responsible AI features

Image classification and IBM Granite are **optional enhancements**!

---

Happy waste sorting! ♻️
