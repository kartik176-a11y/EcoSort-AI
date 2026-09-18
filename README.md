# EcoSort AI ♻️

## Smart Waste Segregation & Disposal Assistant for Sustainable Vizag

[![SDG 11](https://img.shields.io/badge/SDG-11%20Sustainable%20Cities-orange)](https://sdgs.un.org/goals/goal11)
[![SDG 12](https://img.shields.io/badge/SDG-12%20Responsible%20Consumption-green)](https://sdgs.un.org/goals/goal12)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Table of Contents

- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [Features](#features)
- [SDG Alignment](#sdg-alignment)
- [Architecture](#architecture)
- [AI/ML Components](#aiml-components)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Testing](#testing)
- [Limitations](#limitations)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

## 🎯 Problem Statement

Urban households often struggle to correctly identify and segregate mixed waste, leading to:

- **Contamination** of recycling streams
- **Unsafe disposal** of hazardous materials
- **Reduced recycling efficiency**
- **Environmental degradation**
- **Public health risks**

In rapidly growing cities like **Visakhapatnam (Vizag)**, effective household-level waste segregation is critical for:
- Cleaner neighborhoods
- Reduced landfill pressure
- Improved municipal waste management
- Enhanced environmental sustainability

---

## 💡 Solution

**EcoSort AI** is an AI-powered waste segregation assistant that helps citizens:

1. **Classify** waste items using text or image input
2. **Retrieve** relevant disposal guidance from a local knowledge base
3. **Receive** clear, source-grounded recommendations
4. **Understand** uncertainty and limitations through Responsible AI principles

The system combines deterministic classification, retrieval-augmented generation (RAG), and optional LLM integration to provide accurate, grounded guidance.

---

## ✨ Features

### Core Capabilities

✅ **Text-Based Classification**
- Classifies waste into 5 categories: Wet/Biodegradable, Dry/Recyclable, Hazardous/Special Waste, E-Waste, Other/Uncertain
- Handles variations in user input
- Reports confidence levels

✅ **Image-Based Classification** (when model is trained)
- Computer vision using MobileNetV2 architecture
- Detects: cardboard, glass, metal, paper, plastic, trash
- Maps detected classes to EcoSort categories
- Graceful fallback when model unavailable

✅ **RAG (Retrieval-Augmented Generation)**
- Searches local knowledge base documents
- Returns relevant context and source references
- Works offline without external APIs
- Transparent source attribution

✅ **IBM Granite Integration**
- Configurable LLM endpoint support
- Enforces grounding in retrieved evidence
- Prevents hallucination of municipal rules
- **Local fallback** when IBM Granite unavailable

✅ **Responsible AI**
- Clear uncertainty communication
- Explicit warnings for hazardous/special waste
- No fake confidence scores
- Privacy-conscious (images not permanently stored)
- Source transparency

---

## 🌍 SDG Alignment

### Primary: SDG 11 — Sustainable Cities and Communities

EcoSort AI directly supports:
- **11.6**: Reduce adverse environmental impact of cities through waste management
- **11.b**: Integrated policies for resource efficiency

### Secondary: SDG 12 — Responsible Consumption and Production

Contributes to:
- **12.5**: Substantially reduce waste generation through prevention, reduction, recycling, and reuse
- **12.8**: Ensure people have relevant information and awareness for sustainable development

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         USER INPUT                          │
│                  (Text + Optional Image)                    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    CLASSIFICATION                           │
│  ┌──────────────────┐          ┌──────────────────────┐    │
│  │ Text Classifier  │    OR    │  Image Classifier    │    │
│  │  (Keyword-based) │          │  (MobileNetV2 CNN)   │    │
│  └──────────────────┘          └──────────────────────┘    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
                  ┌──────────────┐
                  │   CATEGORY   │
                  │ (5 types)    │
                  └──────┬───────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     RAG RETRIEVAL                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Knowledge Base Search (TF-based similarity)         │  │
│  │  • wet_waste.txt                                     │  │
│  │  • dry_waste.txt                                     │  │
│  │  • hazardous_waste.txt                               │  │
│  │  • e_waste.txt                                       │  │
│  │  • general_guidance.txt                              │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │ RETRIEVED CONTEXT    │
              │ + Source Documents   │
              └──────────┬───────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  LLM GENERATION                             │
│  ┌────────────────────┐         ┌──────────────────────┐   │
│  │  IBM Granite       │   OR    │  Local Fallback      │   │
│  │  (if configured)   │         │  (context passthru)  │   │
│  └────────────────────┘         └──────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  FINAL RECOMMENDATION                       │
│  • Waste Category                                           │
│  • Disposal Instructions                                    │
│  • Grounded Guidance                                        │
│  • Source Documents                                         │
│  • Confidence Level                                         │
│  • Responsible AI Disclaimer                                │
└─────────────────────────────────────────────────────────────┘
```

---

## 🤖 AI/ML Components

### 1. Text Classification

**Approach**: Rule-based keyword matching with normalization

**Categories**:
- **Wet/Biodegradable**: banana peel, food leftovers, vegetable scraps, etc.
- **Dry/Recyclable**: plastic bottle, newspaper, cardboard, glass, metal, etc.
- **Hazardous/Special Waste**: battery, paint, chemicals, expired medicine, etc.
- **E-Waste**: mobile phone, laptop, charger, electronics, etc.
- **Other/Uncertain**: Unknown or ambiguous items

**Confidence**: High, Medium, Low based on keyword match quality

**Files**: `src/classifier.py`

### 2. Image Classification

**Architecture**: MobileNetV2 (pre-trained on ImageNet) + Custom Classification Head

**Model Details**:
- **Input**: 224×224 RGB images
- **Base**: MobileNetV2 (frozen)
- **Head**: GlobalAveragePooling2D → Dropout(0.2) → Dense(6, softmax)
- **Classes**: cardboard, glass, metal, paper, plastic, trash

**Mapping to EcoSort Categories**:
- cardboard, glass, metal, paper, plastic → **Dry/Recyclable**
- trash → **Other/Uncertain**

**Current Status**: Architecture implemented, **trained weights NOT included**

To enable:
1. Install TensorFlow: `pip install tensorflow` or `pip install tensorflow-cpu`
2. Train model on waste dataset (see `models/README.md`)
3. Save weights to `models/waste_classifier.h5`

**Files**: `src/image_classifier.py`, `models/README.md`

### 3. RAG (Retrieval-Augmented Generation)

**Approach**: Term-frequency-based retrieval from local documents

**Workflow**:
1. Load `.txt` and `.pdf` files from `data/` directory
2. Split documents into chunks
3. Index chunks by term frequency
4. Retrieve top-k most relevant chunks for query
5. Return concatenated context + source references

**Graceful Degradation**: Returns "unavailable guidance" message when no matches found

**Files**: `src/rag.py`, `data/`

### 4. LLM Generation (IBM Granite / Local Fallback)

**IBM Granite Mode** (when configured):
- Calls IBM-compatible chat completion endpoint
- System prompt enforces grounding and prevents hallucination
- Returns generated recommendation based on retrieved context

**Local Fallback Mode** (when IBM unavailable):
- Returns retrieved context directly
- Adds clear disclaimer
- Application remains fully functional

**Files**: `src/llm.py`

### 5. Agent Workflow

Orchestrates the complete pipeline:
1. **Classification Agent**: Determines waste category
2. **Retrieval Agent**: Finds relevant guidance
3. **Advisory Agent**: Generates final recommendation

**Files**: `src/agents.py`

---

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- (Optional) TensorFlow 2.15+ for image classification

### Step 1: Clone Repository

```bash
git clone https://github.com/kartik176-a11y/EcoSort-AI.git
cd EcoSort-AI
```

### Step 2: Create Virtual Environment

```bash
python -m venv .venv

# Activate on Linux/macOS:
source .venv/bin/activate

# Activate on Windows:
.venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**For Image Classification** (optional):

```bash
pip install tensorflow
# OR for CPU-only (smaller):
pip install tensorflow-cpu
```

### Step 4: Configure Environment Variables (Optional)

For IBM Granite integration:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
IBM_GRANITE_ENDPOINT=https://your-endpoint.example/v1/chat/completions
IBM_GRANITE_MODEL=ibm-granite
IBM_API_KEY=your_api_key_here
```

**Note**: The app works WITHOUT these credentials using local fallback mode.

---

## 🚀 Usage

### Run the Application

```bash
streamlit run app.py
```

Open your browser to the URL shown (typically `http://localhost:8501`)

### Using the Interface

1. **Enter a waste item** in the text input:
   - Example: "banana peel", "plastic bottle", "used battery"

2. **OR Upload an image** (if model is trained):
   - Supported formats: PNG, JPG, JPEG, WebP

3. Click **🔍 Analyze Waste**

4. View results:
   - **Waste Category**
   - **Detected Item**
   - **Confidence**
   - **Classification Method**
   - **Disposal Recommendation**
   - **Grounded Guidance**
   - **Source Documents**
   - **Retrieved Context** (expandable)

### Example Inputs

**Wet/Biodegradable**:
- banana peel
- food leftovers
- vegetable scraps

**Dry/Recyclable**:
- plastic bottle
- newspaper
- cardboard box
- glass bottle
- metal can

**Hazardous/Special Waste**:
- used battery
- paint can
- expired medicine

**E-Waste**:
- old mobile phone
- laptop
- charger

---

## 📂 Project Structure

```
EcoSort-AI/
│
├── app.py                      # Streamlit application
├── requirements.txt            # Python dependencies
├── run_tests.py               # Test runner
├── README.md                  # This file
├── LICENSE                    # MIT License
├── .gitignore                 # Git exclusions
├── .env.example               # Example environment variables
│
├── src/                       # Source code
│   ├── __init__.py
│   ├── classifier.py          # Text-based waste classifier
│   ├── image_classifier.py    # Image-based classifier (MobileNetV2)
│   ├── rag.py                 # RAG retrieval pipeline
│   ├── llm.py                 # LLM integration (Granite/fallback)
│   ├── agents.py              # Workflow orchestration
│   └── utils.py               # Utility functions
│
├── data/                      # Knowledge base
│   ├── README.md
│   ├── wet_waste.txt          # Wet/biodegradable guidance
│   ├── dry_waste.txt          # Dry/recyclable guidance
│   ├── hazardous_waste.txt    # Hazardous waste guidance
│   ├── e_waste.txt            # E-waste guidance
│   ├── general_guidance.txt   # General/uncertain items
│   ├── official_guidance.txt  # Official sources
│   └── waste_knowledge.txt    # Additional knowledge
│
├── models/                    # Model weights (not in git)
│   └── README.md              # Model documentation
│
├── tests/                     # Test suite
│   ├── test_classifier.py     # Classifier tests
│   ├── test_rag.py            # RAG tests
│   └── test_image_classifier.py  # Image classifier tests
│
├── docs/                      # Additional documentation
│   ├── architecture.md
│   └── responsible_ai.md
│
└── screenshots/               # App screenshots
    └── README.md
```

---

## ⚙️ Configuration

### Environment Variables

Create `.env` file (optional):

| Variable | Description | Required |
|----------|-------------|----------|
| `IBM_GRANITE_ENDPOINT` | IBM Granite API endpoint URL | No |
| `IBM_API_KEY` | IBM API authentication key | No |
| `IBM_GRANITE_MODEL` | Model name/identifier | No |

**Default Behavior**: When variables are not set, the app uses local fallback mode.

### Model Configuration

To enable image classification:
1. Train or obtain weights (see `models/README.md`)
2. Save to `models/waste_classifier.h5`
3. Restart Streamlit app

---

## 🧪 Testing

### Run All Tests

```bash
python run_tests.py
```

### Run Individual Test Suites

```bash
# Text classifier tests
python -m tests.test_classifier

# RAG tests
python -m tests.test_rag

# Image classifier tests
python -m tests.test_image_classifier
```

### Expected Output

```
=== Running Classifier Tests ===
✓ Text normalization works
✓ Wet waste classification works
✓ Dry recyclable classification works
✓ Hazardous waste classification works
✓ E-waste classification works
✓ Uncertain classification works
✓ Empty input handling works
✓ Case insensitivity works
=== All Classifier Tests Passed ✓ ===

=== Running RAG Tests ===
...

=== Running Image Classifier Tests ===
...

=== ALL TESTS PASSED ===
```

---

## ⚠️ Limitations

### Current Limitations

1. **Image Classification Requires Training**
   - Model architecture is implemented
   - Trained weights are NOT included
   - Requires user to train or provide weights

2. **Limited to Household Waste**
   - Designed for common household items
   - Not suitable for industrial/commercial waste

3. **Static Knowledge Base**
   - Documents are pre-loaded, not real-time
   - Requires manual updates for new regulations

4. **Simple Text Matching**
   - Keyword-based, not semantic understanding
   - May miss complex or unusual item descriptions

5. **No Multi-language Support (Yet)**
   - Currently English only
   - Telugu/Hindi support planned for future

6. **RAG Uses Simple TF Scoring**
   - Not embedding-based vector search
   - Good for demo, but could be improved with FAISS/Chroma

7. **Local Deployment Only**
   - Not production-ready for cloud deployment
   - No user authentication or data persistence

### Known Issues

- Large PDF files may slow down RAG initialization
- TensorFlow installation can be large (~500MB)
- No caching of image classification results

---

## 🚀 Future Enhancements

### Planned Features

- [ ] **Multi-language Support**: Telugu, Hindi, other Indian languages
- [ ] **Vector Embeddings**: Upgrade RAG to use FAISS or Chroma
- [ ] **Real-time Training**: Collect user feedback to improve classification
- [ ] **Barcode Scanning**: Auto-classify products by barcode
- [ ] **Location-aware Guidance**: Custom rules by ward/zone in Vizag
- [ ] **Mobile App**: React Native or Flutter version
- [ ] **Voice Input**: Speech-to-text for accessibility
- [ ] **Community Reporting**: Users can report incorrect classifications
- [ ] **Gamification**: Points/badges for proper waste segregation
- [ ] **Integration with GVMC**: Real-time collection schedules and rules

### Possible Improvements

- **Better Image Models**: EfficientNet, Vision Transformer
- **Active Learning**: Continuous model improvement
- **Multi-modal Fusion**: Combine text + image for better accuracy
- **Explainable AI**: Visual attention maps for image classification
- **API Deployment**: REST API for third-party integration

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m 'Add your feature'`
4. Push to branch: `git push origin feature/your-feature`
5. Open a Pull Request

### Areas for Contribution

- Training and sharing waste classification models
- Adding knowledge base documents (especially local Vizag rules)
- Multi-language translations
- UI/UX improvements
- Documentation enhancements
- Bug fixes and testing

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**V. Karthik**

**GitHub**: [@kartik176-a11y](https://github.com/kartik176-a11y)

**Project**: Built for the **1M1B AI for Sustainability Virtual Internship**

**Purpose**: Demonstrating AI/ML for SDG 11 (Sustainable Cities) and SDG 12 (Responsible Consumption)

---

## 🙏 Acknowledgments

- **IBM Granite** for LLM capabilities
- **1M1B Foundation** for the AI for Sustainability initiative
- **GVMC (Greater Visakhapatnam Municipal Corporation)** for municipal waste management guidance
- **Swachh Bharat Mission** for national waste management standards
- **Reference Project**: [vatsalparikh07/garbage-classification-model](https://github.com/vatsalparikh07/garbage-classification-model) for architecture inspiration

---

## 📞 Contact & Support

For questions, issues, or suggestions:

- **GitHub Issues**: [Open an issue](https://github.com/kartik176-a11y/EcoSort-AI/issues)
- **Pull Requests**: Contributions welcome
- **Local Vizag residents**: Contact GVMC for official waste disposal guidance

---

<p align="center">
  <strong>♻️ EcoSort AI — Making Sustainable Waste Management Accessible to All ♻️</strong>
</p>

<p align="center">
  Built with ❤️ for a sustainable future
</p>
