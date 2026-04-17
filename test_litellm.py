import os
from crewai import LLM

# Mock settings
ollama_base_url = "http://localhost:11434"
ollama_model = "qwen3.5:cloud"

os.environ["OPENAI_API_KEY"] = "dummy"

llm = LLM(
    model=f"ollama/{ollama_model}",
    base_url=ollama_base_url
)

print(f"Testing LLM with model: ollama/{ollama_model} and base_url: {ollama_base_url}")

try:
    response = llm.call([{"role": "user", "content": "Say hello"}])
    print(f"LLM response: {response}")
except Exception as e:
    print(f"LLM failed: {e}")
