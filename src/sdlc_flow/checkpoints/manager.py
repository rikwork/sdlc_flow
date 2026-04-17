from typing import Optional
from pathlib import Path
import json

from ..notifications.cli_prompt import CLIPrompt
from ..config import settings, CheckpointStatus


class CheckpointManager:
    def __init__(self, task_dir: Path):
        self.task_dir = task_dir
        self.checkpoint_file = task_dir / "awaiting_human.json"

    def request_approval(self, step_id: str, details: str, force_cli: bool = True) -> bool:
        """
        Request approval for a step. Currently CLI-focused. 
        Telegram logic to be added in Phase 5.
        """
        # Save state to file for audit/resume logic
        checkpoint_data = {
            "step_id": step_id,
            "details": details,
            "status": "waiting"
        }
        with open(self.checkpoint_file, "w") as f:
            json.dump(checkpoint_data, f, indent=2)

        approved = CLIPrompt.approve_step(step_id, details)
        
        # Cleanup or update checkpoint file
        if approved:
            self.checkpoint_file.unlink(missing_ok=True)
        else:
            checkpoint_data["status"] = "rejected"
            with open(self.checkpoint_file, "w") as f:
                json.dump(checkpoint_data, f, indent=2)
                
        return approved

    def get_comment(self) -> str:
        return CLIPrompt.reject_with_comment()
