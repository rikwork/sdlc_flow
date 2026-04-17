from crewai import Agent, Crew, Process, Task


from ..config import settings


class DecompositionCrew:
    def __init__(self, task_id: str = "", workspace_dir: str = "."):
        self.task_id = task_id
        self.workspace_dir = workspace_dir

    def crew(self) -> Crew:
        llm = settings.get_llm("decomposition")

        architect = Agent(
            role="Solution Architect",
            goal="Decompose the selected approach into detailed requirements for task ID: {task_id}",
            backstory="You are an expert in technical breakdown and requirement engineering. You focus on clarity and completeness.",
            allow_delegation=False,
            verbose=True,
            llm=llm
        )

        decomposition_task = Task(
            description="""
                Decompose the following selected approach:
                {selected_approach}
                
                Identify:
                1. Functional requirements (user-facing features)
                2. Technical requirements (database, API, infrastructure)
                3. Acceptance criteria (list of testable points)
                
                Output must be structured and clear.
            """,
            expected_output="Detailed list of functional/technical requirements and acceptance criteria.",
            agent=architect,
        )

        return Crew(
            agents=[architect],
            tasks=[decomposition_task],
            process=Process.sequential,
            verbose=True,
        )
