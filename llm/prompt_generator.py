from __future__ import annotations

from llm.karel_prompt import (
    KarelDSLPromptTemplate,
    KarelPythonPromptTemplate,
    KarelUserPrompt,
)

from llm.minigrid_prompt import (
    MinigridDSLPromptTemplate,
    MinigridPythonPromptTemplate,
    MinigridUserPrompt,
)

from prog_policies.utils import get_env_name

from llm.constant import (
    PYTHON_LIMITATION,
    USER_PROMPT_TEMPLATE_PYTHON_TO_DSL,
    USER_PROMPT_TEMPLATE_DSL,
    USER_PROMPT_TEMPLATE_PYTHON,
)

class PromptGenerator:
    def __init__(
        self,
        task: str,
    ) -> None:
        self.task: str = task
        self.env_name = get_env_name(task)
        self.python_prompt_template = KarelPythonPromptTemplate() if self.env_name == "karel" else MinigridPythonPromptTemplate()
        self.dsl_prompt_template = KarelDSLPromptTemplate() if self.env_name == "karel" else MinigridDSLPromptTemplate()
        self.task_template = KarelUserPrompt(task=task) if self.env_name == "karel" else MinigridUserPrompt(task=task)

    def _env_desc_python(self) -> str:
        return self.python_prompt_template.env_desc
    
    def _env_desc_dsl(self) -> str:
        return self.dsl_prompt_template.env_desc

    def _action_desc_python(self) -> str:
        return self.python_prompt_template.action_desc

    def _preception_desc_python(self) -> str:
        return self.python_prompt_template.perception_desc
    
    def _action_desc_dsl(self) -> str:
        return self.dsl_prompt_template.action_desc

    def _preception_desc_dsl(self) -> str:
        return self.dsl_prompt_template.perception_desc

    def _dsl_desc(self) -> str:
        return self.dsl_prompt_template.dsl_desc

    def _python_limitation(self) -> str:
        return PYTHON_LIMITATION

    def _python_to_dsl(self) -> str:
        return self.python_prompt_template.python_to_dsl

    def get_system_prompt_python_to_dsl(self) -> str:
        system_prompt = (
            self._env_desc_python()
            + "\n"
            + self._action_desc_python()
            + "\n"
            + self._preception_desc_python()
            + "\n"
            + self._python_limitation()
            + "\n"
            + self._python_to_dsl()
        )
        return system_prompt

    def get_user_prompt_python_to_dsl(self) -> str:
        user_prompt = USER_PROMPT_TEMPLATE_PYTHON_TO_DSL.replace("<<task_name>>", self.task.upper()) \
                                                        .replace("<<task_map_desc>>", self.task_template.map_desc) \
                                                        .replace("<<task_agent_position_desc>>", self.task_template.agent_position_desc) \
                                                        .replace("<<task_goal_desc>>", self.task_template.goal_desc) \
                                                        .replace("<<task_return_desc>>", self.task_template.return_desc) \
                                                        .replace("<<environment_name>>", self.env_name.capitalize())
        return user_prompt
    
    def get_system_prompt_python(self) -> str:
        system_prompt = (
            self._env_desc_python()
            + "\n"
            + self._action_desc_python()
            + "\n"
            + self._preception_desc_python()
            + "\n"
            + self._python_limitation()
        )
        return system_prompt
    
    def get_user_prompt_python(self) -> str:
        user_prompt = USER_PROMPT_TEMPLATE_PYTHON.replace("<<task_name>>", self.task.upper()) \
                                                 .replace("<<task_map_desc>>", self.task_template.map_desc) \
                                                 .replace("<<task_agent_position_desc>>", self.task_template.agent_position_desc) \
                                                 .replace("<<task_goal_desc>>", self.task_template.goal_desc) \
                                                 .replace("<<task_return_desc>>", self.task_template.return_desc)
        return user_prompt
    
    def get_system_prompt_dsl(self) -> str:
        system_prompt = (
            self._env_desc_dsl()
            + "\n"
            + self._action_desc_dsl()
            + "\n"
            + self._preception_desc_dsl()
            + "\n"
            + self._dsl_desc()
        )
        return system_prompt

    def get_user_prompt_dsl(self) -> str:
        user_prompt = USER_PROMPT_TEMPLATE_DSL.replace("<<task_name>>", self.task.upper()) \
                                              .replace("<<task_map_desc>>", self.task_template.map_desc) \
                                              .replace("<<task_agent_position_desc>>", self.task_template.agent_position_desc) \
                                              .replace("<<task_goal_desc>>", self.task_template.goal_desc) \
                                              .replace("<<task_return_desc>>", self.task_template.return_desc) \
                                              .replace("<<environment_name>>", self.env_name.capitalize())
        return user_prompt