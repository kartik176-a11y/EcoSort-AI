# 🌱 SustainAI

## AI-Powered Smart Waste Management & Sustainability Assistant

A student AI and sustainability project for the **1M1B AI for Sustainability Virtual Internship in collaboration with IBM SkillsBuild and AICTE**.

SustainAI supports **SDG 12 — Responsible Consumption and Production** and **SDG 11 — Sustainable Cities and Communities**.

## Features

- Nine-category waste classification with confidence and uncertainty handling
- Disposal guidance, sustainability impact, and sustainable actions
- Local knowledge-base retrieval (simple lexical RAG)
- Conversational assistant with session-only history
- Optional configurable LLM endpoint with a clearly labelled fallback
- Responsible AI safeguards and no unnecessary personal-data collection

No image analysis is implemented or simulated.

## Project structure

```text
EcoSort-AI/
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── data/waste_knowledge.txt
├── src/{classifier.py, rag.py, llm.py, utils.py}
└── docs/{architecture.md, responsible_ai.md}
```

## Run locally

```bash
git clone https://github.com/kartik176-a11y/EcoSort-AI.git
cd EcoSort-AI
python -m venv .venv
```

Windows: `\.venv\\Scripts\\activate`  
macOS/Linux: `source .venv/bin/activate`

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app works without credentials in local RAG fallback mode. To configure a compatible endpoint, copy `.env.example` to `.env` and load those variables in your environment. Never commit real keys.

## Test

Try: plastic bottle, plastic wrapper, newspaper, cardboard, banana peel, food waste, vegetable waste, glass bottle, aluminium can, steel can, old phone, laptop, charger, battery, headphones, old clothes, mixed waste, unknown object, an ambiguous description, and empty input. Empty and unknown inputs should not crash and should return **Uncertain** where appropriate.

## Limitations

Classification and retrieval are simple prototypes; local rules vary; knowledge coverage is limited; and the app is not an official waste-management authority. Future ideas include embeddings, municipal-policy retrieval, multilingual support, computer vision, and repair recommendations.

## Author

- Name: _Add your name_
- College: _Add your college_
