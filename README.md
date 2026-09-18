# EcoSort AI — Smart Waste Segregation & Disposal Assistant

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

EcoSort AI is a simple Streamlit prototype that helps citizens classify common household waste items, retrieve relevant local guidance from a small grounded knowledge base, and obtain a concise recommendation. It uses a transparent multi-stage workflow with waste classification, retrieval, and advisory generation.

## Features

- Text-based waste classification
- Optional image upload with preview-only handling
- Deterministic categorization for common household items
- RAG-style retrieval using local documents and demo guidance
- LLM-backed generation through a configurable Granite-compatible interface
- Grounded recommendation with visible source references
- Responsible AI warnings for uncertainty and hazardous waste
- Demo mode when external APIs or documents are unavailable

## AI architecture

User Input
→ Input Analysis
→ Waste Classification
→ RAG Retrieval
→ Granite / LLM Generation
→ Source-Grounded Recommendation

The app keeps the classification deterministic and constrains the final answer to the retrieved evidence, avoiding unsupported municipal claims.

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

1. Classification Agent
   - Determines the likely category for a waste item.
2. Retrieval Agent
   - Finds relevant official or reference guidance.
3. Advisory Agent
   - Produces a concise, source-grounded answer for the user.

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

## Technology stack

- Python
- Streamlit
- PyPDF
- Requests
- Local demo knowledge base / retrieval layer
- Optional Granite-compatible LLM integration via environment variables

## Project structure

```text
EcoSort-AI/
├── app.py
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── data/
│   ├── README.md
│   ├── official_guidance.txt
│   ├── gvms/
│   │   └── gvmc_guidance.txt
│   └── swachh_bharat/
│       └── swachh_bharat_guidance.txt
├── docs/
│   ├── architecture.md
│   └── responsible_ai.md
├── prompts/
│   └── advisory_prompt.txt
├── screenshots/
│   └── README.md
├── src/
│   ├── __init__.py
│   ├── agents.py
│   ├── classifier.py
│   ├── granite.py
│   ├── rag.py
│   └── utils.py
└── .venv/
```

## Installation

```bash
git clone https://github.com/kartik176-a11y/EcoSort-AI.git
cd EcoSort-AI
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

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

Then open the local Streamlit URL shown in the terminal.

## Example inputs and expected output

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
- Expected: Hazardous/Special waste or E-waste, with a warning not to place it in ordinary household waste

## Future scope

- Add true image recognition for common household items
- Add user-friendly municipal rule mapping by ward or zone
- Improve retrieval with FAISS or Chroma embeddings
- Add multilingual support for Telugu and English
- Extend the knowledge base with real GVMC and local authority documents

## Demo instructions

1. Run the app locally with `streamlit run app.py`.
2. Enter one of the example waste items.
3. Press Analyze waste.
4. Review the category, recommendation, retrieved sources, and responsible-AI warning.
5. If needed, test the demo mode by leaving the Granite environment variables unset.

## Author and internship context

This project is designed for the 1M1B AI for Sustainability Virtual Internship, with a focus on the SDG goals and a simple, local prototype suitable for a short demonstration.
