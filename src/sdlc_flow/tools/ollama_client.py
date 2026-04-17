import requests
from ..config import settings


def generate(prompt: str, model: str | None = None, stream: bool = False) -> str:
    """Generate text using Ollama HTTP API.

    Args:
        prompt: The prompt to send to the model.
        model: Model name; defaults to the one configured in settings.
        stream: Whether to request a streaming response (default ``False``).

    Returns:
        The generated text as a string.
    """
    if model is None:
        model = settings.ollama_model

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": stream,
    }

    url = f"{settings.ollama_base_url}/api/generate"
    response = requests.post(url, json=payload)
    response.raise_for_status()
    data = response.json()
    # Ollama returns the generated text under the ``response`` key when not streaming.
    return data.get("response", "")
