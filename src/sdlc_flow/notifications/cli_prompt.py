from typing import List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt

console = Console()


class CLIPrompt:
    @staticmethod
    def approve_step(step_name: str, details: str) -> bool:
        console.print(Panel(f"[bold green]Approval Required: {step_name}[/bold green]\n\n{details}"))
        return Confirm.ask(f"Do you approve {step_name}?")

    @staticmethod
    def reject_with_comment() -> str:
        return Prompt.ask("Please provide comments for rejection")

    @staticmethod
    def report_status(status_msg: str) -> None:
        console.print(f"[bold blue]INFO:[/bold blue] {status_msg}")

    @staticmethod
    def report_error(error_msg: str) -> None:
        console.print(f"[bold red]ERROR:[/bold red] {error_msg}")
