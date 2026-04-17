from crewai import Agent, Crew, Process, Task
from ..config import settings


class DocsCrew:
    def __init__(self, task_id: str = "", workspace_dir: str = "."):
        self.task_id = task_id
        self.workspace_dir = workspace_dir

    def crew(self) -> Crew:
        llm = settings.get_llm("docs")

        writer = Agent(
            role="Technical Writer",
            goal="Generate comprehensive documentation for the task {task_id}",
            backstory="Expert in creating clear, concise, and useful documentation for developers and users.",
            verbose=True,
            llm=llm
        )

        docs_task = Task(
            description="""
                Generate documentation based on:
                - Implementation results: {implementation}
                - Tech Spec: {tech_spec}
                - API Contract: {api_contract}
                
                Include:
                1. Overview
                2. Installation/Usage instructions
                3. API Documentation
                4. Code summary
            """,
            expected_output="Final documentation files in Markdown format.",
            agent=writer,
        )

        return Crew(
            agents=[writer],
            tasks=[docs_task],
            process=Process.sequential,
            verbose=True,
        )
