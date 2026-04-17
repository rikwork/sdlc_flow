import subprocess
from crewai_tools import BaseTool


class LintTool(BaseTool):
    name: str = "Lint Tool"
    description: str = "Runs static analysis (ruff, eslint) on the codebase via subprocess."

    def _run(self, linter: str, path: str) -> str:
        """Runs the specified linter."""
        try:
            if linter == "ruff":
                cmd = f"ruff check {path}"
            elif linter == "eslint":
                # Assuming node_modules is present
                cmd = f"./node_modules/.bin/eslint {path}"
            else:
                return f"Error: Unsupported linter '{linter}'."

            result = subprocess.run(
                cmd, 
                shell=True, 
                capture_output=True, 
                text=True
            )
            
            if result.returncode == 0:
                return f"{linter} passed successfully on {path}"
            else:
                return f"{linter} found issues:\n{result.stdout}\n{result.stderr}"
        except Exception as e:
            return f"Linter execution failed: {str(e)}"
