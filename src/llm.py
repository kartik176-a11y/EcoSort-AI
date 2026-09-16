"""Optional LLM adapter with an honest local fallback."""
import os
import requests


def llm_is_configured():
    return bool(os.getenv("IBM_GRANITE_ENDPOINT") and os.getenv("IBM_API_KEY"))


def fallback_response(question, context):
    return ("I am using the local knowledge-base RAG fallback, not IBM Granite.\n\n"
            f"Relevant retrieved knowledge:\n\n{context}\n\n"
            "Waste rules vary by location, so verify the final route with a local service.")


def generate_response(question, context):
    if not llm_is_configured():
        return fallback_response(question, context), "fallback"
    payload = {"model": os.getenv("IBM_GRANITE_MODEL", "ibm-granite"), "messages": [{"role": "system", "content": "Answer only from the supplied context. State uncertainty, avoid unsafe instructions, and recommend checking local rules."}, {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}], "temperature": 0.2}
    try:
        response = requests.post(os.environ["IBM_GRANITE_ENDPOINT"], json=payload, headers={"Authorization": f"Bearer {os.environ['IBM_API_KEY']}"}, timeout=20)
        response.raise_for_status()
        answer = response.json().get("choices", [{}])[0].get("message", {}).get("content")
        if answer:
            return answer, "llm"
    except (requests.RequestException, ValueError, KeyError, IndexError):
        pass
    return fallback_response(question, context), "fallback"
