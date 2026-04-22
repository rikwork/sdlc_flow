from crewai import Agent, Crew, Process, Task


from ..config import settings


from ..tools.file_tool import SafeFileWriteTool
from ..tools.shell_tool import ShellTool
from crewai_tools import FileReadTool, DirectorySearchTool

class BackendCrew:
    def __init__(self, task_id: str, workspace_dir: str, rag_db_path: str = ""):
        self.task_id = task_id
        self.workspace_dir = workspace_dir
        self.rag_db_path = rag_db_path

    def crew(self) -> Crew:
        llm = settings.get_llm("backend_dev")
        
        file_write_tool = SafeFileWriteTool(
            task_id=self.task_id, 
            workspace_dir=self.workspace_dir,
            rag_db_path=self.rag_db_path
        )
        file_read_tool = FileReadTool(workspace_dir=self.workspace_dir)
        dir_search_tool = DirectorySearchTool(workspace_dir=self.workspace_dir)
        shell_tool = ShellTool()

        dev = Agent(
            role="Backend Developer",
            goal="Implement backend logic for task {task_id} according to TechSpec and API contract",
            backstory="Expert Python developer. You write clean, testable, and efficient code following PEP 8 and architectural best practices.",
            verbose=True,
            tools=[file_write_tool, file_read_tool, dir_search_tool, shell_tool],
            llm=llm
        )

        dev_task = Task(
            description="""
                Implement the following technical specification:
                {tech_spec}
                
                API Contract:
                {api_contract}
                
                Semantic Codebase Context:
                {rag_context}
                
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
