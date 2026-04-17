import subprocess
import time
import signal
import os
from crewai_tools import BaseTool
from typing import Optional


class MockServerTool(BaseTool):
    name: str = "Mock Server Tool"
    description: str = "Starts a mock server from an OpenAPI contract (api_contract.yaml) using Prism."
    process: Optional[subprocess.Popen] = None

    def _run(self, contract_path: str, port: int = 4010) -> str:
        """Starts the mock server."""
        try:
            cmd = f"npx stoplight/prism mock {contract_path} -p {port}"
            self.process = subprocess.Popen(
                cmd, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid
            )
            # Wait a bit for server to start
            time.sleep(3)
            return f"Mock server started on http://localhost:{port} from {contract_path}"
        except Exception as e:
            return f"Failed to start mock server: {str(e)}"

    def stop(self) -> str:
        """Stops the mock server."""
        if self.process:
            os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
            return "Mock server stopped."
        return "No mock server running."
