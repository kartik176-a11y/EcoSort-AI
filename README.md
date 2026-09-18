# 🌱 ♻️ EcoSort AI 🌍 — Smart Waste Segregation & Disposal Assistant

## Problem statement

Urban households often struggle to identify mixed waste correctly, resulting in contamination of recycling streams, unsafe disposal of hazardous items, and lower environmental impact. This is especially important in cities such as Visakhapatnam (Vizag), where better household segregation can support cleaner neighborhoods and stronger waste-management outcomes.

## Why this matters in Vizag

Visakhapatnam is growing rapidly, and sustainable urban waste management is important for local sanitation, public health, and environmental resilience. Better segregation at the household level can reduce landfill pressure, improve recycling, and support cleaner public spaces.

## SDG alignment

- SDG 11 — Sustainable Cities and Communities
- SDG 12 — Responsible Consumption and Production

## Target users

- Households and local residents
- Community waste awareness programs
- Local volunteers and school clubs
- Municipal/NGO awareness and education teams

## Solution

EcoSort AI is an intelligent Streamlit application that helps citizens classify household waste items using **text descriptions or images**, retrieve relevant local guidance from a grounded knowledge base, and obtain a concise, responsible recommendation. It uses a transparent multi-stage workflow with waste classification, retrieval-augmented generation (RAG), and LLM advisory.

## Features

### 🆕 Image Classification (NEW!)
- **Real waste image recognition** using InceptionV3 neural network
- Upload photos of waste items for automatic classification
- Top-5 prediction display for transparency
- Maps ImageNet classes to EcoSort waste categories
- Graceful fallback to text classification when TensorFlow unavailable

### Core Features
- Text-based waste classification with keyword matching
- RAG-style retrieval using local documents and guidance
- LLM-backed generation through a configurable Granite-compatible interface
- Grounded recommendation with visible source references
- Responsible AI warnings for uncertainty and hazardous waste
- Demo mode when external APIs or documents are unavailable

### Waste Categories
1. **Wet/Biodegradable** — Food waste, organic matter
2. **Dry/Recyclable** — Paper, plastic, glass, metal
3. **Hazardous/Special waste** — Batteries, chemicals, paint
4. **E-waste** — Electronics, phones, laptops
5. **Other/Uncertain** — Items requiring verification

## AI architecture

```
User Input (Text/Image)
      ↓
IMAGE CLASSIFICATION (InceptionV3)
   OR TEXT CLASSIFICATION
      ↓
WASTE CATEGORY DETECTION
      ↓
RAG RETRIEVAL
      ↓
GRANITE / LLM GENERATION
      ↓
SOURCE-GROUNDED RECOMMENDATION
      ↓
RESPONSIBLE AI DISCLAIMER
```

The app keeps the classification evidence-based and constrains the final answer to retrieved context, avoiding unsupported municipal claims.

## Image Classification Workflow

```
UPLOAD IMAGE
      ↓
IMAGE PREPROCESSING
  - Resize to 299×299
  - RGB conversion
  - InceptionV3 normalization
      ↓
INCEPTIONV3 PREDICTION
  - Trained on ImageNet
  - Top-5 object classes
      ↓
CATEGORY MAPPING
  - Map detected objects to waste categories
  - Example: "plastic_bottle" → Dry/Recyclable
  - Example: "banana" → Wet/Biodegradable
      ↓
RAG RETRIEVAL + LLM GUIDANCE
      ↓
DISPOSAL RECOMMENDATION
```

**Note:** Image classification uses pre-trained InceptionV3 weights from TensorFlow/Keras. No large model files are committed to the repository.

## RAG workflow

The system includes a lightweight retrieval layer that:

- Loads text or PDF-based documents from the `data/` folder
- Extracts document text
- Splits documents into chunks
- Builds an in-memory vector-style index using term-frequency similarity
- Retrieves the most relevant sections for a given waste item
- Passes the retrieved evidence to the advisory stage

If the system cannot use an external vector database, it falls back to a local demo index so the prototype still runs.

## Agent workflow

The workflow is intentionally transparent and sequential:

1. **Classification Agent**
   - Image classification (if image uploaded and TensorFlow available)
   - Text classification (if text provided or image classification unavailable)
   - Determines the likely category for a waste item
   
2. **Retrieval Agent**
   - Finds relevant official or reference guidance
   - Uses detected item name for semantic search
   
3. **Advisory Agent**
   - Produces a concise, source-grounded answer for the user
   - Uses Granite LLM or local fallback

## IBM Granite role

IBM Granite provides a configurable generation layer when appropriate environment variables are set. The system prompt enforces:

- Use only retrieved context
- Do not invent municipal rules
- Do not claim unsupported facts
- State uncertainty if evidence is insufficient
- Give concise and understandable guidance
- Clearly distinguish official guidance from general advice
- Mention the supporting sources

## Responsible AI

The app is designed to communicate uncertainty instead of guessing. It displays visible disclaimers for:

- special or hazardous waste
- ambiguous items
- incomplete evidence
- local municipal verification requirements
- image-upload privacy expectations
- model limitations and confidence scores

**Image Classification Notes:**
- InceptionV3 is trained on general objects (ImageNet), not waste-specific datasets
- Always verify critical decisions (hazardous, e-waste) with local authorities
- Images are processed locally and not stored by default
- Top-5 predictions shown for transparency

## Technology stack

- **Python** — Core language
- **Streamlit** — Web interface
- **TensorFlow/Keras** — Image classification (InceptionV3)
- **Pillow** — Image processing
- **NumPy** — Array operations
- **PyPDF** — PDF document parsing
- **Requests** — HTTP client for LLM APIs
- **Local RAG** — Knowledge retrieval layer
- **IBM Granite** — Optional LLM integration

## Project structure

```text
EcoSort-AI/
├── app.py                          # Main Streamlit application
├── README.md
├── requirements.txt                # Dependencies (includes TensorFlow)
├── .env.example
├── .gitignore
├── data/                           # Knowledge base documents
│   ├── README.md
│   ├── official_guidance.txt
│   ├── gvms/
│   │   └── gvmc_guidance.txt
│   └── swachh_bharat/
│       └── swachh_bharat_guidance.txt
├── docs/
│   ├── architecture.md
│   ├── responsible_ai.md
│   └── image_classification.md     # 🆕 Image classification docs
├── prompts/
│   └── advisory_prompt.txt
├── screenshots/
│   └── README.md
├── src/
│   ├── __init__.py
│   ├── agents.py                   # ✏️ Updated: image + text workflow
│   ├── classifier.py               # Text classification
│   ├── image_classifier.py         # 🆕 Image classification module
│   ├── granite.py
│   ├── llm.py
│   ├── rag.py
│   └── utils.py
└── .venv/
```

## Installation

### Full Installation (with image classification)

```bash
git clone https://github.com/kartik176-a11y/EcoSort-AI.git
cd EcoSort-AI
git checkout feature/waste-image-classification  # Or main after merge
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**Note:** 
- TensorFlow download is ~500 MB
- First run downloads InceptionV3 weights (~154 MB) automatically
- Use `tensorflow-cpu` for smaller install size (CPU-only)

### Minimal Installation (text-only)

```bash
pip install streamlit requests pypdf
```

The app will work in text-classification mode. Image classification will show as unavailable.

## Environment variables

Copy the example file and fill in values if using a compatible model endpoint:

```bash
cp .env.example .env
```

```dotenv
IBM_GRANITE_ENDPOINT=https://your-compatible-granite-endpoint.example/v1/chat/completions
IBM_GRANITE_MODEL=ibm-granite
IBM_API_KEY=your_api_key_here
```

If these are not set, the app automatically enters demo mode and still works without external credentials.

## How to run

```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal (typically `http://localhost:8501`).

### First Run Notes

- TensorFlow will download InceptionV3 weights on first image classification (one-time)
- Initial model loading takes 5-10 seconds
- Subsequent classifications are faster (model cached in memory)

## Example inputs and expected output

### Text Classification Examples

Example 1:
- Input: `banana peel`
- Expected: Wet/Biodegradable waste

Example 2:
- Input: `plastic bottle`
- Expected: Dry/Recyclable waste

Example 3:
- Input: `newspaper`
- Expected: Dry/Recyclable waste

Example 4:
- Input: `used battery`
- Expected: Hazardous/Special waste, with warning

Example 5:
- Input: `old mobile phone`
- Expected: E-waste

### Image Classification Examples

**Try uploading photos of:**

- Plastic bottles → Dry/Recyclable
- Fresh fruits/vegetables → Wet/Biodegradable
- Cardboard boxes → Dry/Recyclable
- Glass bottles → Dry/Recyclable
- Metal cans → Dry/Recyclable
- Mobile phones/laptops → E-waste

**Note:** Image classification works best with:
- Clear, well-lit photos
- Single object in focus
- Minimal background clutter

## Integration Details

### Source Repository

This implementation integrates the waste classification approach from [vatsalparikh07/garbage-classification-model](https://github.com/vatsalparikh07/garbage-classification-model).

**Key Finding:** The source repository does **not** contain trained model weights. It only has training code and app structure.

### Our Approach

Since no trained model was available, we implemented:
- InceptionV3 pre-trained on ImageNet (automatic download)
- Intelligent mapping from ImageNet classes to waste categories
- Transparent top-5 predictions
- Graceful degradation when TensorFlow unavailable

See [`docs/image_classification.md`](docs/image_classification.md) for complete technical details.

## Future scope

- ✅ ~~Add true image recognition for common household items~~ (COMPLETED)
- Fine-tune model on waste-specific datasets
- Add support for multiple image uploads
- Add user-friendly municipal rule mapping by ward or zone
- Improve retrieval with FAISS or Chroma embeddings
- Add multilingual support for Telugu and English
- Extend the knowledge base with real GVMC and local authority documents
- Collect user feedback for model improvement

## Demo instructions

1. Run the app locally with `streamlit run app.py`
2. **Option A:** Enter a waste item description (text)
3. **Option B:** Upload an image of waste
4. **Option C:** Use both text + image for verification
5. Press "Analyze Waste"
6. Review:
   - Classification method (image/text)
   - Detected item and category
   - Confidence and reasoning
   - Top predictions (for images)
   - Disposal recommendation
   - Retrieved source documents
   - Responsible AI disclaimer

## Testing

### Test Image Classification

```bash
# Test with TensorFlow installed
python -c "from src.image_classifier import is_available; print('Image classification:', 'Available' if is_available() else 'Unavailable')"

# Test classification
python -c "from src.image_classifier import classify_waste_image; from PIL import Image; result = classify_waste_image(Image.new('RGB', (299, 299))); print(result)"
```

### Test Text Classification

```bash
python -c "from src.classifier import classify_text_item; print(classify_text_item('plastic bottle'))"
```

## Troubleshooting

### Image classification not working

**Problem:** "Image classification unavailable" message

**Solution:** Install TensorFlow:
```bash
pip install tensorflow>=2.13.0
```

Or for CPU-only (smaller):
```bash
pip install tensorflow-cpu>=2.13.0
```

### TensorFlow import errors

**Problem:** Module not found or version conflicts

**Solution:**
- Ensure Python 3.8-3.11 (TensorFlow compatibility)
- Update pip: `pip install --upgrade pip`
- Reinstall: `pip uninstall tensorflow && pip install tensorflow>=2.13.0`

### First run is slow

**Problem:** Takes 10-30 seconds on first image classification

**Solution:** This is normal. InceptionV3 weights are being downloaded and cached. Subsequent runs are faster.

### Low confidence predictions

**Solution:**
- Use clearer, well-lit images
- Focus on single object
- Try different angles
- Verify with text classification
- Check top-5 predictions for alternatives

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Test your changes
4. Submit a pull request

## Author and internship context

This project is designed for the **1M1B AI for Sustainability Virtual Internship**, with a focus on SDG goals and practical waste management solutions for Vizag.

**Prepared by:** V.Karthik

## License

MIT License - See LICENSE file for details

## Acknowledgments

- Image classification approach inspired by [vatsalparikh07/garbage-classification-model](https://github.com/vatsalparikh07/garbage-classification-model)
- InceptionV3 model by Google (via TensorFlow/Keras)
- IBM Granite for LLM integration
- Streamlit for rapid prototyping
