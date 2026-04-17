import os
from crewai_tools import BaseTool


class FileTool(BaseTool):
    name: str = "File Tool"
    description: str = "Perform file operations (read, write, list) within the project directory."

    def _run(self, action: str, file_path: str, content: str = "") -> str:
        """Runs a file operation."""
        try:
            full_path = os.path.abspath(file_path)
            if action == "read":
                if not os.path.exists(full_path):
                    return f"Error: File {file_path} does not exist."
                with open(full_path, "r") as f:
                    return f.read()
            elif action == "write":
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, "w") as f:
                    f.write(content)
                return f"File {file_path} written successfully."
            elif action == "list":
                if not os.path.isdir(full_path):
                    return f"Error: {file_path} is not a directory."
                return "\n".join(os.listdir(full_path))
            else:
                return f"Error: Unknown action '{action}'."
        except Exception as e:
            return f"File operation failed: {str(e)}"
