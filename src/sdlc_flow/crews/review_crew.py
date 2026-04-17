from crewai import Agent, Crew, Process, Task


from ..config import settings


class ReviewCrew:
    def __init__(self, task_id: str = "", workspace_dir: str = "."):
        self.task_id = task_id
        self.workspace_dir = workspace_dir

    def crew(self) -> Crew:
        llm = settings.get_llm("reviewer")

        reviewer = Agent(
            role="Senior Software Engineer",
            goal="Provide thorough peer review for task {task_id} (Iteration {iteration})",
            backstory="Expert at identifying edge cases, potential security vulnerabilities, and performance bottlenecks.",
            verbose=True,
            llm=llm
        )

        review_task = Task(
            description="""
                Review the following changes introduced in iteration {iteration}:
                {changes}
                
                Requirements to check against:
                {requirements}
                
                Provide a clear 'APPROVED' or 'REJECTED' with detailed comments and action items.
            """,
            expected_output="A review report with approval status and comments.",
            agent=reviewer,
        )

        return Crew(
            agents=[reviewer],
            tasks=[review_task],
            process=Process.sequential,
            verbose=True,
        )
