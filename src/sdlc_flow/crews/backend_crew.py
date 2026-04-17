from crewai import Agent, Crew, Process, Task


from ..config import settings


class BackendCrew:
    def crew(self) -> Crew:
        llm = settings.get_llm("backend_dev")

        dev = Agent(
            role="Backend Developer",
            goal="Implement backend logic for task {task_id} according to TechSpec and API contract",
            backstory="Expert Python developer. You write clean, testable, and efficient code following PEP 8 and architectural best practices.",
            verbose=True,
            llm=llm
        )

        dev_task = Task(
            description="""
                Implement the following technical specification:
                {tech_spec}
                
                API Contract:
                {api_contract}
                
                Ensure the code is complete, includes unit tests, and follows the project structure.
            """,
            expected_output="Finished source code and tests.",
            agent=dev,
        )

        return Crew(
            agents=[dev],
            tasks=[dev_task],
            process=Process.sequential,
            verbose=True,
        )
