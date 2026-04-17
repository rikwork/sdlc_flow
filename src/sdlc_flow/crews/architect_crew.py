from crewai import Agent, Crew, Process, Task


from ..config import settings


class ArchitectCrew:
    def __init__(self, task_id: str = "", workspace_dir: str = "."):
        self.task_id = task_id
        self.workspace_dir = workspace_dir

    def crew(self) -> Crew:
        llm = settings.get_llm("architect")

        analyst = Agent(
            role="System Analyst",
            goal="Research existing codebase and context to write TechSpec.md",
            backstory="Expert in system analysis. You use specialized tools to understand the current architecture.",
            verbose=True,
            llm=llm
        )
        tech_lead = Agent(
            role="Tech Lead",
            goal="Review TechSpec and ensure architectural consistency for task {task_id}",
            backstory="Experienced technical leader. You ensure that the proposed solution is scalable and maintainable.",
            verbose=True,
            llm=llm
        )
        api_designer = Agent(
            role="API Designer",
            goal="Generate api_contract.yaml (OpenAPI 3.0) based on requirements",
            backstory="Expert in RESTful API design and OpenAPI specifications.",
            verbose=True,
            llm=llm
        )

        arch_task = Task(
            description="""
                Based on the requirements:
                {requirements}
                
                1. System Analyst: Research context and draft TechSpec.md.
                2. API Designer: Create api_contract.yaml.
                3. Tech Lead: Review and finalize the architectural design.
                
                Platforms to consider: {platforms}
                
                At the end of your document, strictly include these exact lines based on your design decisions:
                Needs API: [true/false]
                Needs UI: [true/false]
            """,
            expected_output="Final TechSpec.md and api_contract.yaml with Needs API/UI flags appended.",
            agent=tech_lead,
        )

        return Crew(
            agents=[analyst, tech_lead, api_designer],
            tasks=[arch_task],
            process=Process.hierarchical,
            manager_llm=llm,
            verbose=True,
        )
