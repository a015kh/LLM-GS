from .constant import (
    PYTHON_LIMITATION,
)


class SystemPromptTemplate:
    def __init__(
        self, env_name: str = "karel", language: str = "python"
    ):
        self.env_name = env_name
        self.language = language

    ### System Prompt ###
    @property
    def env_desc(self) -> str:
        raise NotImplementedError("Subclasses should implement this method.")

    @property
    def action_desc(self) -> str:
        raise NotImplementedError("Subclasses should implement this method.")

    @property
    def perception_desc(self) -> str:
        raise NotImplementedError("Subclasses should implement this method.")

    @property
    def dsl_desc(self) -> str:
        raise NotImplementedError("Subclasses should implement this method.")

    @property
    def python_to_dsl(self) -> str:
        raise NotImplementedError("Subclasses should implement this method.")


class UserPromptTemplate:
    def __init__(self, task: str):
        self.task = task

    ### User Prompt ###
    @property
    def task_map_desc(self) -> str:
        raise NotImplementedError("Subclasses should implement this method.")

    @property
    def task_agent_position_desc(self) -> str:
        raise NotImplementedError("Subclasses should implement this method.")

    @property
    def task_goal_desc(self) -> str:
        raise NotImplementedError("Subclasses should implement this method.")

    @property
    def task_return_desc(self) -> str:
        raise NotImplementedError("Subclasses should implement this method.")
