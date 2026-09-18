from pathlib import Path
import os

import streamlit as st

from src.agents import run_waste_workflow
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
        if os.getenv("IBM_GRANITE_ENDPOINT") and os.getenv("IBM_API_KEY"):
            st.success("Granite mode configured")
        else:
            st.info("Demo mode: local fallback active")
        st.markdown("---")
        st.markdown("### Responsible AI")
        st.caption("Guidance is informational. Verify special or hazardous waste instructions with authorized local authorities.")


def render_result(result):
    st.markdown("---")
    st.subheader("Analysis result")
    left, right = st.columns(2)
    with left:
        st.metric("Waste category", result["category"])
        st.write(f"**Detected item:** {result['detected_item']}")
        st.write(f"**Confidence:** {result['confidence']}")
        st.write(f"**Reason:** {result['reason']}")
    with right:
        st.success(f"**Disposal recommendation**\n\n{result['recommendation']}")
        st.info(f"**Grounded guidance**\n\n{result['grounded_guidance']}")

    st.markdown("**Source documents**")
    for source in result.get("sources", []):
        st.write(f"- {source}")

    if result.get("disclaimer"):
        st.warning(result["disclaimer"])
    if result.get("demo_label"):
        st.caption(result["demo_label"])
    with st.expander("Retrieval context used"):
        st.write(result["retrieved_context"])


render_sidebar()
st.title("EcoSort AI ♻️")
st.subheader("Smart Waste Segregation Assistant for Sustainable Vizag")
st.write("Identify a household waste item, retrieve relevant local guidance, and receive a concise source-grounded recommendation.")

left, right = st.columns([1.6, 1])
with left:
    item = st.text_input("Enter a waste item or question", placeholder="Try: banana peel, plastic bottle, used battery")
    image_file = st.file_uploader(
        "Optional image upload (preview only; no computer vision is performed)",
        type=["png", "jpg", "jpeg", "webp"],
    )
    if image_file is not None:
        st.image(image_file, caption="Preview only — the image is not stored by this app.", use_container_width=True)
    analyze = st.button("Analyze Waste", type="primary", use_container_width=True)

with right:
    st.markdown("### Demo examples")
    st.markdown("banana peel  \nplastic bottle  \nnewspaper  \nused battery  \nfood leftovers  \ncardboard box")

if analyze:
    if not item.strip():
        st.warning("Please enter a waste item or question.")
    else:
        render_result(run_waste_workflow(item, image_file=image_file, rag_pipeline=get_rag_pipeline()))

st.markdown("---")
st.subheader("Responsible AI")
st.markdown(
    "- AI guidance does not replace official municipal instructions.\n"
    "- Recommendations use retrieved knowledge-base context when available.\n"
    "- The system does not invent municipal rules and reports uncertainty.\n"
    "- Special, hazardous, battery, and e-waste instructions must be verified locally.\n"
    "- No unnecessary personal information is collected.\n"
    "- Uploaded images are preview-only and are not permanently stored by default."
)
