from crewai import Agent, Crew, Process, Task


from ..config import settings


class BrainstormCrew:
    def __init__(self, task_id: str = "", workspace_dir: str = "."):
        self.task_id = task_id
        self.workspace_dir = workspace_dir

    def crew(self) -> Crew:
        llm = settings.get_llm("brainstorm")
        
        analyst = Agent(
            role="Product Analyst",
            goal="Identify the best approach for the given task: {task_description}",
            backstory="You are an expert in software product analysis. You think outside the box and consider all technical implications.",
            allow_delegation=False,
            verbose=True,
            llm=llm
        )

        brainstorm_task = Task(
            description="""
                Brainstorm 3 different approaches for the following task:
                {task_description}
                
                Context: {context}
                
                For each approach, provide:
                1. Title
                2. Implementation idea
                3. Pros and Cons
                
                Select the best approach and explain why.
                
                At the very end of your report, strictly classify the task complexity and include exactly one of these lines:
                Complexity: simple
                Complexity: medium
                Complexity: complex
            """,
            expected_output="A structured report with 3 approaches, pros/cons, and a final selection.",
            agent=analyst,
        )

        return Crew(
            agents=[analyst],
            tasks=[brainstorm_task],
            process=Process.sequential,
            verbose=True,
        )
