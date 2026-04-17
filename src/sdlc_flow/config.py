from enum import Enum
from pathlib import Path
from typing import Optional, Any

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class CheckpointStatus(str, Enum):
    ON = "ON"
    OFF = "OFF"


class LLMConfig(BaseModel):
    brainstorm: str = "qwen3.5:cloud"
    decomposition: str = "qwen3.5:cloud"
    architect: str = "qwen3.5:cloud"
    backend_dev: str = "qwen3.5:cloud"
    web_dev: str = "qwen3.5:cloud"
    mobile_dev: str = "qwen3.5:cloud"
    reviewer: str = "qwen3.5:cloud"
    qa: str = "qwen3.5:cloud"
    docs: str = "qwen3.5:cloud"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen3.5:cloud"

    # Dynamic project root
    project_root_path: Path = Field(default_factory=lambda: Path(__file__).resolve().parent.parent.parent)
    tasks_store_path: Path = Path("tasks")

    approve_scope: CheckpointStatus = CheckpointStatus.ON
    approve_architecture: CheckpointStatus = CheckpointStatus.ON
    qa_report_auto_approve: CheckpointStatus = CheckpointStatus.OFF

    telegram_bot_token: Optional[str] = None
    telegram_chat_id: Optional[str] = None

    llm: LLMConfig = LLMConfig()

    def get_llm(self, stage: Optional[str] = None) -> Any:
        from crewai import LLM
        model_name = getattr(self.llm, stage) if stage else self.ollama_model
        # Use liteLLM format: ollama/<model>
        import os
        os.environ["OPENAI_API_KEY"] = "dummy"
        os.environ["OLLAMA_API_BASE"] = self.ollama_base_url
        return LLM(
            model=f"ollama/{model_name}", 
            base_url=self.ollama_base_url,
            timeout=300,
            max_retries=3
        )

settings = Settings()
