import streamlit as st

from src.classifier import EXAMPLES, classify_waste
from src.llm import generate_response, llm_is_configured
from src.rag import load_knowledge, retrieve

st.set_page_config(page_title="SustainAI", page_icon="🌱", layout="wide")


def show_result(result, context):
    st.subheader("Analysis result")
    left, right = st.columns(2)
    with left:
        st.metric("Likely category", result["category"])
        st.write(f"**Confidence:** {result['confidence']}")
        st.write(f"**Why this classification?** {result['reason']}")
    with right:
        st.info(f"**Disposal guidance**\n\n{result['guidance']}")
        st.success(f"**Sustainability impact**\n\n{result['impact']}")
    st.write(f"**Sustainable action:** {result['action']}")
    with st.expander("Relevant knowledge retrieved"):
        st.write(context)
    if result["category"] == "Uncertain":
        st.warning("This result is uncertain. Verify local guidance before disposal.")


knowledge = load_knowledge()
st.title("🌱 SustainAI")
st.subheader("AI-Powered Smart Waste Management & Sustainability Assistant")
st.write("Classify waste and learn about reduction, reuse, recycling, and responsible disposal.")
st.caption("SDG 12 — Responsible Consumption and Production | SDG 11 — Sustainable Cities and Communities")

with st.sidebar:
    page = st.radio("Navigate", ["Home", "Waste Analyzer", "Chat Assistant", "About"])
    if llm_is_configured():
        st.success("Mode: configured LLM")
    else:
        st.info("Mode: local RAG fallback (no LLM configured)")

if page == "Home":
    st.header("Make better waste decisions")
    st.write("SustainAI combines transparent classification with retrieval from a small local sustainability knowledge base.")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("SDG 12")
        st.write("Encourages responsible consumption, reuse, repair, and recycling.")
    with col2:
        st.subheader("SDG 11")
        st.write("Supports cleaner, safer, and more sustainable communities.")

elif page == "Waste Analyzer":
    st.header("Waste Analyzer")
    example = st.selectbox("Try an example", ["Choose an example"] + EXAMPLES)
    description = st.text_area("Describe the waste item", value="" if example == "Choose an example" else example, max_chars=500)
    if st.button("Analyze waste", type="primary", use_container_width=True):
        if not description.strip():
            st.warning("Please enter a description first.")
        else:
            show_result(classify_waste(description), retrieve(description, knowledge))

elif page == "Chat Assistant":
    st.header("Sustainability Chat Assistant")
    st.write("Ask a question. The app retrieves relevant local knowledge before answering.")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    prompt = st.chat_input("How should I handle an old phone?")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        context = retrieve(prompt, knowledge)
        answer, _ = generate_response(prompt, context)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()

else:
    st.header("About SustainAI")
    st.write("A student project for the 1M1B AI for Sustainability Virtual Internship with IBM SkillsBuild and AICTE.")
    st.subheader("Responsible AI")
    st.markdown("- No unnecessary personal information is requested.\n- Results communicate uncertainty.\n- Guidance is general and not official local policy.\n- Unsafe instructions are avoided.\n- Verify local requirements and use human judgment.")

st.divider()
st.caption("Prototype guidance only. Check local waste requirements before disposal.")
