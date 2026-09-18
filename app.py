import os
from pathlib import Path

import streamlit as st

from src.agents import run_waste_workflow
from src.rag import RAGPipeline

st.set_page_config(page_title="EcoSort AI ♻️", page_icon="♻️", layout="wide")


def build_sidebar():
    with st.sidebar:
        st.image("https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?auto=format&fit=crop&w=1200&q=80", use_container_width=True)
        st.markdown("### EcoSort AI")
        st.markdown("Smart Waste Segregation Assistant for Sustainable Vizag")
        st.caption("SDG 11 • SDG 12")
        if os.getenv("IBM_GRANITE_ENDPOINT") and os.getenv("IBM_API_KEY"):
            st.success("Granite/LLM configured")
        else:
            st.info("Demo mode active — using local grounded fallback")
        st.markdown("---")
        st.markdown("### Responsible AI")
        st.caption("AI guidance is for support only and must be checked against official local rules for special waste.")


if "rag_pipeline" not in st.session_state:
    st.session_state.rag_pipeline = RAGPipeline(data_dir=Path(__file__).resolve().parent / "data")

build_sidebar()

st.title("EcoSort AI ♻️")
st.subheader("Smart Waste Segregation Assistant for Sustainable Vizag")
st.caption("A simple RAG-grounded prototype for household waste categorization and disposal guidance.")

with st.container():
    st.markdown(
        "This prototype helps identify common household waste, assigns a likely segregation category, retrieves official guidance, and produces a concise recommendation grounded in the current knowledge base."
    )

col1, col2 = st.columns([1.5, 1])

with col1:
    st.markdown("### Check a waste item")
    item_text = st.text_input(
        "Enter the item or question",
        value="banana peel",
        placeholder="Try: banana peel, plastic bottle, newspaper, used battery",
    )

    uploaded_file = st.file_uploader(
        "Optional: upload a waste image",
        type=["png", "jpg", "jpeg", "webp"],
        help="The image is used only for local preview; it is not stored by default."
    )

    if uploaded_file is not None:
        st.image(uploaded_file, caption=f"Uploaded: {uploaded_file.name}", use_container_width=True)

    submit = st.button("Analyze waste", type="primary", use_container_width=True)

with col2:
    st.markdown("### Demo examples")
    examples = [
        "banana peel",
        "plastic bottle",
        "newspaper",
        "used battery",
        "food leftovers",
        "cardboard box",
    ]
    for example in examples:
        st.code(example)

result_container = st.container()

if submit:
    if not item_text.strip():
        st.warning("Please enter a waste item or question before analyzing.")
    else:
        result = run_waste_workflow(
            item=item_text.strip(),
            image_file=uploaded_file,
            rag_pipeline=st.session_state.rag_pipeline,
        )
        with result_container:
            st.markdown("---")
            st.markdown("### Result")
            st.markdown(f"**Detected / identified item:** {result['detected_item']}")
            st.markdown(f"**Waste category:** {result['category']}")
            st.markdown(f"**Confidence:** {result['confidence']}")
            st.markdown(f"**Reason:** {result['reason']}")
            st.markdown(f"**Disposal recommendation:** {result['recommendation']}")

            if result.get("sources"):
                st.markdown("**Source documents:**")
                for source in result["sources"]:
                    st.markdown(f"- {source}")

            st.markdown("**Grounded guidance:**")
            st.info(result["grounded_guidance"])

            if result.get("disclaimer"):
                st.warning(result["disclaimer"])

            if result.get("demo_label"):
                st.caption(result["demo_label"])

            with st.expander("Retrieval context used"):
                st.write(result["retrieved_context"])

st.markdown("---")

st.markdown("### Responsible AI")
st.markdown(
    "- AI guidance does not replace official municipal instructions.\n"
    "- The response is grounded in retrieved sources shown in the app.\n"
    "- Special or hazardous waste should be checked with authorized local authorities.\n"
    "- No unnecessary personal information is collected or stored.\n"
    "- Uploaded images are not retained by default.\n"
    "- Uncertain waste categories are reported as uncertain rather than guessed.\n"
    "- If reliable guidance is unavailable, the app clearly states it."
)

st.markdown("### Data / knowledge basis")
st.markdown(
    "The application uses a local knowledge base based on official waste-management themes, GVMC-style guidance, and Swachh Bharat material, with a demo fallback when external APIs are unavailable."
)
