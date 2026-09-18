from pathlib import Path
import os

import streamlit as st

from src.agents import run_waste_workflow
from src.rag import RAGPipeline

# Try to import image classifier for status checking
try:
    from src.image_classifier import get_classification_status
    IMAGE_STATUS_AVAILABLE = True
except ImportError:
    IMAGE_STATUS_AVAILABLE = False


st.set_page_config(page_title="EcoSort AI ♻️", page_icon="♻️", layout="wide")

DATA_DIR = Path(__file__).resolve().parent / "data"


@st.cache_resource
def get_rag_pipeline():
    return RAGPipeline(DATA_DIR)


def render_sidebar():
    with st.sidebar:
        st.markdown("## EcoSort AI ♻️")
        st.caption("Smart Waste Segregation Assistant for Sustainable Vizag")
        st.markdown("**SDG 11:** Sustainable Cities and Communities  \n**SDG 12:** Responsible Consumption and Production")
        
        st.markdown("---")
        st.markdown("### System Status")
        
        # IBM Granite status
        if os.getenv("IBM_GRANITE_ENDPOINT") and os.getenv("IBM_API_KEY"):
            st.success("✓ IBM Granite configured")
        else:
            st.info("ℹ Local fallback mode (no IBM Granite)")
        
        # Image classification status
        if IMAGE_STATUS_AVAILABLE:
            status = get_classification_status()
            if status['available']:
                st.success("✓ Image classification ready")
            else:
                st.warning(f"⚠ Image: {status['reason']}")
        else:
            st.warning("⚠ Image classification unavailable")
        
        st.markdown("---")
        st.markdown("### Responsible AI")
        st.caption("Guidance is informational. Verify special or hazardous waste instructions with authorized local authorities.")


def render_result(result):
    st.markdown("---")
    st.subheader("Analysis Result")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Waste Category", result["category"])
        st.write(f"**Detected Item:** {result['detected_item']}")
        st.write(f"**Confidence:** {result['confidence']}")
        st.write(f"**Classification Method:** {result['reason']}")
    
    with col2:
        st.success(f"**Disposal Recommendation**\n\n{result['recommendation']}")
        st.info(f"**Grounded Guidance**\n\n{result['grounded_guidance']}")

    st.markdown("**Source Documents**")
    if result.get("sources"):
        for source in result["sources"]:
            st.write(f"- {source}")
    else:
        st.write("- No specific sources found")

    if result.get("disclaimer"):
        st.warning(result["disclaimer"])
    
    if result.get("demo_label"):
        st.caption(f"💡 Response mode: {result['demo_label']}")
    
    with st.expander("📄 View Retrieved Context"):
        st.text(result["retrieved_context"])


# Main UI
render_sidebar()

st.title("EcoSort AI ♻️")
st.subheader("Smart Waste Segregation & Disposal Assistant for Sustainable Vizag")
st.write("Identify household waste items, retrieve relevant local guidance, and receive source-grounded recommendations.")

col_left, col_right = st.columns([1.6, 1])

with col_left:
    item = st.text_input(
        "Enter a waste item or question",
        placeholder="Try: banana peel, plastic bottle, used battery, old mobile phone"
    )
    
    image_file = st.file_uploader(
        "Upload an image of waste (optional)",
        type=["png", "jpg", "jpeg", "webp"],
        help="Upload a waste image for computer vision classification (if model is available)"
    )
    
    if image_file is not None:
        st.image(image_file, caption="Uploaded Image", use_container_width=True)
    
    analyze = st.button("🔍 Analyze Waste", type="primary", use_container_width=True)

with col_right:
    st.markdown("### 📝 Example Inputs")
    st.markdown("""
    **Wet/Biodegradable:**
    - banana peel
    - food leftovers
    
    **Dry/Recyclable:**
    - plastic bottle
    - newspaper
    - cardboard box
    - glass bottle
    - metal can
    
    **Hazardous:**
    - used battery
    - paint can
    
    **E-Waste:**
    - old mobile phone
    - charger
    - laptop
    """)

if analyze:
    if not item.strip() and image_file is None:
        st.warning("⚠ Please enter a waste item or upload an image.")
    else:
        with st.spinner("Analyzing waste..."):
            result = run_waste_workflow(
                item, 
                image_file=image_file, 
                rag_pipeline=get_rag_pipeline()
            )
        render_result(result)

# Responsible AI Section
st.markdown("---")
st.subheader("🛡 Responsible AI")
st.markdown("""
- **AI recommendations are informational** and do not replace official municipal instructions.
- The system uses **retrieved knowledge base context** when available and reports uncertainty when evidence is insufficient.
- **Special, hazardous, battery, and e-waste** require local verification with authorized authorities.
- **Image classification** (when available) uses a computer vision model trained on waste categories.
- **No personal information** is collected. Uploaded images are processed in memory only and not permanently stored.
- **IBM Granite integration** (when configured) provides enhanced language generation while maintaining grounding in retrieved evidence.
- When IBM Granite is unavailable, the system uses a **local fallback** that still provides useful guidance.
""")

st.markdown("---")
st.caption("Built for SDG 11 (Sustainable Cities) and SDG 12 (Responsible Consumption) | EcoSort AI by V.Karthik")
