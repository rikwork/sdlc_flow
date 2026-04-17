import subprocess
from crewai_tools import BaseTool

class ShellTool(BaseTool):
    name: str = "Shell Tool"
    description: str = "Runs shell commands (ruff, mypy, pytest) to validate code quality and correctness."

    def _run(self, command: str) -> str:
        """Executes a shell command safely."""
        # Note: In a real production system, we'd want more strict command validation here.
        # But for this SDLC Flow transformation, we'll allow standard dev tools.
        allowed_tools = ["ruff", "mypy", "pytest", "python"]
        if not any(tool in command for tool in allowed_tools):
             return f"Error: Command '{command}' is not in the allowed pool: {allowed_tools}"
             
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True
            )
            
            output = result.stdout + "\n" + result.stderr
            status = "SUCCESS" if result.returncode == 0 else "FAILED"
            return f"Command: {command}\nStatus: {status}\nOutput:\n{output}"
        except Exception as e:
            return f"Execution failed: {str(e)}"
