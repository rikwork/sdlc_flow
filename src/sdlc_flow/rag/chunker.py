import ast
from pathlib import Path
from typing import List, Dict

def chunk_python_file(file_path: Path) -> List[Dict]:
    """Parses a Python file and extracts functions/classes as chunks."""
    try:
        content = file_path.read_text(encoding="utf-8")
        tree = ast.parse(content, filename=str(file_path))
    except Exception as e:
        # If it fails to parse (e.g. invalid syntax), return generic chunk
        if file_path.exists():
            return [{"text": file_path.read_text(encoding="utf-8"), "metadata": {"file": str(file_path)}}]
        return []

    chunks = []
    
    # Split into classes and top-level functions
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            start_line = node.lineno - 1
            end_line = node.end_lineno
            lines = content.splitlines()
            chunk_text = "\n".join(lines[start_line:end_line])
            if chunk_text.strip():
                chunks.append({
                    "text": chunk_text,
                    "metadata": {
                        "file": str(file_path),
                        "type": type(node).__name__,
                        "name": node.name
                    }
                })
    
    # Fallback if no classes/functions found but file has content
    if not chunks and content.strip():
        chunks.append({
            "text": content,
            "metadata": {"file": str(file_path), "type": "module"}
        })
        
    return chunks

def chunk_file(file_path: Path) -> List[Dict]:
    """Dispatcher for different file types."""
    ext = file_path.suffix.lower()
    if ext in [".py"]:
        return chunk_python_file(file_path)
    elif ext in [".js", ".jsx", ".ts", ".tsx"]:
        # Basic chunking for JS/TS since python ast doesn't work for JS
        content = file_path.read_text(encoding="utf-8")
        return [{"text": content, "metadata": {"file": str(file_path), "type": "js_file"}}]
    else:
        # Fallback raw file
        if file_path.exists():
            return [{"text": file_path.read_text(encoding="utf-8"), "metadata": {"file": str(file_path), "type": "generic"}}]
        return []
