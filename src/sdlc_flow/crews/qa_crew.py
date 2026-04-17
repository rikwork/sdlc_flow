from crewai import Agent, Crew, Process, Task
from ..config import settings


class QACrew:
    def __init__(self, task_id: str = "", workspace_dir: str = "."):
        self.task_id = task_id
        self.workspace_dir = workspace_dir

    def crew(self) -> Crew:
        llm = settings.get_llm("qa")

        tester = Agent(
            role="QA Engineer",
            goal="Verify the implementation against acceptance criteria for task {task_id}",
            backstory="Expert in automated testing and manual verification. You use browser tools to click through the UI if needed.",
            verbose=True,
            llm=llm
        )

        qa_task = Task(
            description="""
                Verify the following implementation:
                {implementation}
                
                Acceptance Criteria:
                {acceptance_criteria}
                
                Run tests and provide a detailed report on which criteria passed or failed.
            """,
            expected_output="Detailed QA report with pass/fail status for each criterion.",
            agent=tester,
        )

        return Crew(
            agents=[tester],
            tasks=[qa_task],
            process=Process.sequential,
            verbose=True,
        )
