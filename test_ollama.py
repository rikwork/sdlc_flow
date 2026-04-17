import sys
import os
from pathlib import Path

# Add src to sys.path
src_path = Path(__file__).resolve().parent / "src"
sys.path.append(str(src_path))

from sdlc_flow.tools.ollama_client import generate

try:
    response = generate("Write a 3-sentence brainstorm about a calculator app.")
    print(f"Ollama response: {response}")
except Exception as e:
    print(f"Error connecting to Ollama: {e}")
