import os

import requests


UNAVAILABLE_GUIDANCE = (
    "Reliable guidance was not found in the current knowledge base. "
    "Please verify disposal instructions with the local municipal authority."
)

SYSTEM_PROMPT = (
    "You are the EcoSort AI advisory assistant. Use only the retrieved context. "
    "Do not invent municipal rules or unsupported claims. If evidence is insufficient, "
    "say that reliable guidance was not found. Be concise, distinguish general guidance "
    "from official requirements, and mention the source."
)


def llm_is_configured():
    return bool(os.getenv("IBM_GRANITE_ENDPOINT", "").strip() and os.getenv("IBM_API_KEY", "").strip())


def fallback_response(question, context):
    if not context or context.startswith("Reliable guidance was not found"):
        return UNAVAILABLE_GUIDANCE
    return (
        "Local demo guidance (not IBM Granite):\n\n"
        f"{context}\n\n"
        "Verify the final disposal route with the local municipal authority, especially for special or hazardous waste."
    )


def generate_response(question, context):
    if not llm_is_configured():
        return fallback_response(question, context), "fallback"

    payload = {
        "model": os.getenv("IBM_GRANITE_MODEL", "ibm-granite"),
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Question: {question}\nRetrieved context:\n{context}"},
        ],
    }
    try:
        response = requests.post(
            os.environ["IBM_GRANITE_ENDPOINT"],
            json=payload,
            headers={"Authorization": f"Bearer {os.environ['IBM_API_KEY']}", "Content-Type": "application/json"},
            timeout=20,
        )
        response.raise_for_status()
        content = response.json().get("choices", [{}])[0].get("message", {}).get("content")
        if content and str(content).strip():
            return str(content).strip(), "granite"
    except (requests.RequestException, ValueError, KeyError, IndexError, TypeError):
        pass
    return fallback_response(question, context), "fallback"
