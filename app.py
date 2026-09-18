from pathlib import Path
import os

import streamlit as st

from src.agents import run_waste_workflow, IMAGE_CLASSIFICATION_AVAILABLE
from src.rag import RAGPipeline

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
        
        # Show system capabilities
        st.markdown("---")
        st.markdown("### System Capabilities")
        if os.getenv("IBM_GRANITE_ENDPOINT") and os.getenv("IBM_API_KEY"):
            st.success("✓ Granite LLM configured")
        else:
            st.info("○ Demo mode: local fallback active")
        
        if IMAGE_CLASSIFICATION_AVAILABLE:
            st.success("✓ Image classification enabled")
        else:
            st.warning("○ Image classification unavailable\n\nInstall TensorFlow to enable:\n```pip install tensorflow```")
        
        st.markdown("---")
        st.markdown("### Responsible AI")
        st.caption("Guidance is informational. Verify special or hazardous waste instructions with authorized local authorities.")


def render_result(result):
    st.markdown("---")
    st.subheader("🔍 Analysis Result")
    
    # Show classification method
    method = result.get("classification_method", "text")
    if method == "image":
        st.info("🖼️ **Classification Method:** Image Recognition using InceptionV3")
    elif method == "text":
        st.info("📝 **Classification Method:** Text-based Classification")
    else:
        st.info("**Classification Method:** Fallback")
    
    left, right = st.columns(2)
    with left:
        st.metric("🗑️ Waste Category", result["category"])
        st.write(f"**Detected Item:** {result['detected_item']}")
        st.write(f"**Confidence:** {result['confidence']}")
        st.write(f"**Analysis:** {result['reason']}")
        
        # Show image classification details if available
        if "image_details" in result:
            with st.expander("📊 Image Classification Details"):
                st.write(f"**Model:** {result['image_details'].get('model', 'Unknown')}")
                st.write("**Top 5 Predictions:**")
                for i, pred in enumerate(result['image_details'].get('top_predictions', []), 1):
                    st.write(f"{i}. {pred['class']} — {pred['confidence']}")
    
    with right:
        st.success(f"**♻️ Disposal Recommendation**\n\n{result['recommendation']}")
        st.info(f"**📚 Grounded Guidance**\n\n{result['grounded_guidance']}")

    st.markdown("**📄 Source Documents**")
    if result.get("sources"):
        for source in result["sources"]:
            st.write(f"- {source}")
    else:
        st.write("- No specific source documents found")

    if result.get("disclaimer"):
        st.warning(f"⚠️ {result['disclaimer']}")
    if result.get("demo_label"):
        st.caption(f"System mode: {result['demo_label']}")
    
    with st.expander("🔍 View Retrieval Context"):
        st.write(result["retrieved_context"])


render_sidebar()

st.title("🌱 EcoSort AI ♻️")
st.subheader("Smart Waste Segregation & Disposal Assistant for Sustainable Vizag")

# Feature highlight
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("📝 **Text Classification**")
    st.caption("Enter waste item name")
with col2:
    st.markdown("🖼️ **Image Recognition**")
    st.caption("Upload waste photo")
with col3:
    st.markdown("📚 **RAG Retrieval**")
    st.caption("Grounded guidance")

st.markdown("---")

# Main input area
left, right = st.columns([1.6, 1])
with left:
    item = st.text_input(
        "🔤 Enter a waste item or question (optional if uploading image)", 
        placeholder="Try: banana peel, plastic bottle, used battery",
        help="Describe the waste item you want to classify"
    )
    
    image_file = st.file_uploader(
        "📷 Upload waste image (supports real classification with TensorFlow)",
        type=["png", "jpg", "jpeg", "webp"],
        help="Upload a clear photo of the waste item for automatic classification"
    )
    
    if image_file is not None:
        st.image(image_file, caption="Uploaded image for classification", use_container_width=True)
        if IMAGE_CLASSIFICATION_AVAILABLE:
            st.success("✓ Image will be analyzed using InceptionV3 neural network")
        else:
            st.warning("⚠️ Image classification unavailable. Install TensorFlow to enable: `pip install tensorflow`")
    
    analyze = st.button("🔍 Analyze Waste", type="primary", use_container_width=True)

with right:
    st.markdown("### 💡 Try These Examples")
    st.markdown("""
    **Wet/Biodegradable:**
    - banana peel
    - food leftovers
    - vegetable scraps
    
    **Dry/Recyclable:**
    - plastic bottle
    - newspaper
    - cardboard box
    - glass bottle
    
    **Hazardous:**
    - used battery
    - paint can
    
    **E-waste:**
    - old mobile phone
    - laptop
    """)

if analyze:
    if not item.strip() and image_file is None:
        st.warning("⚠️ Please enter a waste item description or upload an image.")
    else:
        with st.spinner("🔄 Analyzing waste item..."):
            result = run_waste_workflow(item, image_file=image_file, rag_pipeline=get_rag_pipeline())
            render_result(result)

st.markdown("---")
st.subheader("🤖 Responsible AI Principles")
st.markdown("""
- ✓ AI guidance does not replace official municipal instructions
- ✓ Recommendations use retrieved knowledge-base context when available
- ✓ The system does not invent municipal rules and reports uncertainty
- ✓ Special, hazardous, battery, and e-waste instructions must be verified locally
- ✓ No unnecessary personal information is collected
- ✓ Uploaded images are processed locally and not permanently stored by default
- ✓ Image classification uses InceptionV3 pre-trained on ImageNet for object recognition
""")

st.markdown("---")
st.caption("Built with ❤️ for Sustainable Vizag | Prepared by: V.Karthik")
