# Changelog

All notable changes to EcoSort AI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-09-18

### Added

#### Core Features
- **Real Image Classification Module** (`src/image_classifier.py`)
  - MobileNetV2-based architecture for waste image classification
  - 6 waste classes: cardboard, glass, metal, paper, plastic, trash
  - Graceful fallback when model weights unavailable
  - Clear mapping from detected classes to EcoSort categories
  - Status checking and availability reporting

- **Enhanced Text Classification** (`src/classifier.py`)
  - Keyword-based classification for 5 waste categories
  - Normalization and case-insensitive matching
  - Confidence level reporting (High/Medium/Low)
  - Robust handling of empty/unknown inputs

- **RAG Knowledge Base**
  - `data/wet_waste.txt` - Comprehensive wet/biodegradable guidance
  - `data/dry_waste.txt` - Dry/recyclable materials guidance
  - `data/hazardous_waste.txt` - Hazardous waste handling
  - `data/e_waste.txt` - Electronic waste disposal
  - `data/general_guidance.txt` - Uncertain items and mixed materials

- **Integrated Workflow** (`src/agents.py`)
  - Smart prioritization: Image → Text → Fallback
  - Combined classification from multiple sources
  - Clear indication of classification method used
  - Seamless RAG retrieval and LLM generation

- **Enhanced Streamlit UI** (`app.py`)
  - System status indicators (Granite + Image classification)
  - Improved layout with examples sidebar
  - Clear visual hierarchy for results
  - Expanded Responsible AI section
  - Retrieved context viewer

#### Testing
- **Comprehensive Test Suite**
  - `tests/test_classifier.py` - Text classification tests
  - `tests/test_rag.py` - RAG retrieval tests
  - `tests/test_image_classifier.py` - Image classifier tests
  - `run_tests.py` - Unified test runner

#### Documentation
- **README.md** - Complete project documentation
  - Architecture diagrams
  - Installation and usage instructions
  - AI/ML component descriptions
  - Limitations and future enhancements
  - SDG alignment details

- **models/README.md** - Model training guide
  - How to enable image classification
  - Training code examples
  - Dataset recommendations
  - Pre-trained weights guidance

#### Infrastructure
- **Updated `.gitignore`** - Comprehensive exclusions for model files, environments, and temporary files
- **Updated `requirements.txt`** - All dependencies with optional TensorFlow
- **Tests Package** - Proper `tests/__init__.py` for package structure

### Changed
- **agents.py**: Integrated real image classification with priority-based workflow
- **app.py**: Enhanced UI with status indicators and improved result display
- **requirements.txt**: Added Pillow, numpy, and optional TensorFlow dependencies

### Fixed
- Image upload handling now properly detects when TensorFlow is unavailable
- Classification workflow no longer claims image processing when it's not happening
- RAG retrieval handles empty queries gracefully
- All modules handle missing dependencies without crashing

### Architecture Decisions

**Why MobileNetV2 instead of InceptionV3?**
- Lighter weight (~14 MB vs ~90 MB)
- Faster inference
- Better suited for deployment
- Reference repo doesn't actually provide InceptionV3 weights

**Why keyword-based text classification?**
- Deterministic and transparent
- No model training required
- Works offline
- Suitable for demo and prototype

**Why local fallback for LLM?**
- Ensures app always works
- No external API dependency
- User can test without credentials
- Transparent about capabilities

**Why NOT include trained weights?**
- Model files too large for git (10-20 MB)
- No suitable public weights found that match architecture
- Better to let users train on their own dataset
- Avoids licensing/copyright issues

---

## [0.1.0] - Initial Version (Pre-Enhancement)

### Initial Features
- Basic text classification
- Simple RAG retrieval
- IBM Granite integration
- Local fallback mode
- Streamlit UI prototype

---

## Future Versions (Planned)

### [1.1.0] - Planned
- Multi-language support (Telugu, Hindi)
- Vector embedding-based RAG (FAISS/Chroma)
- Improved test coverage
- Performance optimizations

### [2.0.0] - Future
- Trained model weights
- Real-time learning from user feedback
- Mobile app version
- API deployment
- GVMC integration
