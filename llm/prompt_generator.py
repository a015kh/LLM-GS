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
from prog_policies.utils.indent import str_to_indent_python, node_to_indent_python
from prog_policies.base import dsl_nodes
from prog_policies.base import BaseDSL

from llm.constant import (
    PYTHON_LIMITATION,
    USER_PROMPT_TEMPLATE_PYTHON_TO_DSL,
    USER_PROMPT_TEMPLATE_DSL,
    USER_PROMPT_TEMPLATE_PYTHON,
    REVISION_REGENERATION_WITH_REWARD,
    REVISION_REGENERATION,
    REVISION_AGENT_EXECUTION_TRACE,
    REVISION_AGENT_PROGRAM_EXECUTION_TRACE,
)


class PromptGenerator:
    def __init__(
        self,
        task: str,
        action_shots: int = 0,
        perception_shots: int = 0,
        program_shots: int = 0,
    ) -> None:
        self.task: str = task
        self.env_name = get_env_name(task)
        self.python_prompt_template = (
            KarelPythonPromptTemplate()
            if self.env_name == "karel"
            else MinigridPythonPromptTemplate()
        )
        self.dsl_prompt_template = (
            KarelDSLPromptTemplate()
            if self.env_name == "karel"
            else MinigridDSLPromptTemplate()
        )
        self.task_template = (
            KarelUserPrompt(task=task)
            if self.env_name == "karel"
            else MinigridUserPrompt(task=task)
        )

        # Revision parameters
        self.action_shots = action_shots
        self.perception_shots = perception_shots
        self.program_shots = program_shots

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
        user_prompt = (
            USER_PROMPT_TEMPLATE_PYTHON_TO_DSL.replace(
                "<<task_name>>", self.task.upper()
            )
            .replace("<<task_map_desc>>", self.task_template.map_desc)
            .replace(
                "<<task_agent_position_desc>>", self.task_template.agent_position_desc
            )
            .replace("<<task_goal_desc>>", self.task_template.goal_desc)
            .replace("<<task_return_desc>>", self.task_template.return_desc)
            .replace("<<environment_name>>", self.env_name.capitalize())
        )
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
        user_prompt = (
            USER_PROMPT_TEMPLATE_PYTHON.replace("<<task_name>>", self.task.upper())
            .replace("<<task_map_desc>>", self.task_template.map_desc)
            .replace(
                "<<task_agent_position_desc>>", self.task_template.agent_position_desc
            )
            .replace("<<task_goal_desc>>", self.task_template.goal_desc)
            .replace("<<task_return_desc>>", self.task_template.return_desc)
        )
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
        user_prompt = (
            USER_PROMPT_TEMPLATE_DSL.replace("<<task_name>>", self.task.upper())
            .replace("<<task_map_desc>>", self.task_template.map_desc)
            .replace(
                "<<task_agent_position_desc>>", self.task_template.agent_position_desc
            )
            .replace("<<task_goal_desc>>", self.task_template.goal_desc)
            .replace("<<task_return_desc>>", self.task_template.return_desc)
            .replace("<<environment_name>>", self.env_name.capitalize())
        )
        return user_prompt

    ### Revision ###

    def get_user_prompt_revision_regeneration_with_reward(
        self,
        progs_rewards: list[list[dsl_nodes.Program, float]],
        dsl: BaseDSL,
        program_nums: int = 5,
    ) -> str:

        candidate_program_str_and_reward = set(
            (node_to_indent_python(program), reward)
            for sub in progs_rewards
            for (program, reward) in sub
        )
        candidate_program_str_and_reward = sorted(
            candidate_program_str_and_reward, key=lambda x: x[1], reverse=True
        )
        high_score_program = ""
        i = 0
        for program_str, reward in candidate_program_str_and_reward:
            i += 1
            high_score_program += f"""
            Program {i}:
            {program_str}
            reward:
            {reward}
            """

        user_prompt = (
            REVISION_REGENERATION_WITH_REWARD.replace("<<task_name>>", self.task.upper())
            .replace("<<task_map_desc>>", self.task_template.map_desc)
            .replace(
                "<<task_agent_position_desc>>", self.task_template.agent_position_desc
            )
            .replace("<<task_goal_desc>>", self.task_template.goal_desc)
            .replace("<<task_return_desc>>", self.task_template.return_desc)
            .replace("<<programs>>", high_score_program)
        )

        return user_prompt

    def get_user_prompt_revision_regeneration(
        self, program_list: list[dsl_nodes.Program], dsl: BaseDSL
    ):
        program_str_list = [dsl.parse_node_to_str(p) for p in program_list]
        program_str_set = set(program_str_list)

        programs = ""

        for i, program_str in enumerate(program_str_set):

            programs += f"Program {i+1}:\n"
            programs += str_to_indent_python(program_str, dsl) + "\n"

        user_prompt = (
            REVISION_REGENERATION.replace("<<task_name>>", self.task.upper())
            .replace("<<task_map_desc>>", self.task_template.map_desc)
            .replace(
                "<<task_agent_position_desc>>", self.task_template.agent_position_desc
            )
            .replace("<<task_goal_desc>>", self.task_template.goal_desc)
            .replace("<<task_return_desc>>", self.task_template.return_desc)
            .replace("<<programs>>", programs)
        )
        return user_prompt

    def get_user_prompt_revision_agent_execution_trace(
        self,
        reward: float,
        logs: list[dict[str, str]],
        average_reward: float,
        max_steps: int = 50,
    ) -> str:
        initial_state = logs[0]["state"]

        trajectory = ""

        for i, log in enumerate(logs):
            if i == 0 or i >= max_steps:
                continue
            trajectory += f"Step {i}:\n"
            if log["type"] == "action":
                trajectory += f"Agent performs an action: {log['name']}." + "\n"
            elif log["type"] == "perception":
                trajectory += (
                    f"Agent performs a perception: {log['name']}. The result is {log['result']}."
                    + "\n"
                )
            trajectory += "Partial state:" + "\n"
            trajectory += log["state"] + "\n"

            try:
                if abs(log["instant_reward"]) >= 0.000001:
                    trajectory += (
                        f"The agent got a reward of {log['instant_reward']}\n\n"
                    )
                else:
                    trajectory += "\n"
            except:
                trajectory += "\n"

        if len(logs[1:]) >= max_steps:
            trajectory += f"The total step number is {len(logs[1:])}, the latter ones are truncated."

        user_prompt = (
            REVISION_AGENT_EXECUTION_TRACE.replace("<<task_name>>", self.task.upper())
            .replace("<<task_map_desc>>", self.task_template.map_desc)
            .replace(
                "<<task_agent_position_desc>>", self.task_template.agent_position_desc
            )
            .replace("<<task_goal_desc>>", self.task_template.goal_desc)
            .replace("<<task_return_desc>>", self.task_template.return_desc)
            .replace("<<initial_state>>", initial_state)
            .replace("<<trajectory>>", trajectory)
            .replace("<<reward>>", str(reward))
            .replace("<<program>>", logs[0]["program_str"])
            .replace("<<average_reward>>", str(average_reward))
        )
        return user_prompt

    def get_user_prompt_revision_agent_program_execution_trace(
        self,
        reward: float,
        logs: list[dict[str, str]],
        average_reward: float,
        max_steps: int = 50,
    ) -> str:
        initial_state = logs[0]["state"]

        trajectory = ""

        for i, log in enumerate(logs):
            if i == 0 or i >= max_steps:
                continue
            trajectory += f"Step {i}:\n"
            trajectory += "Program:\n"
            trajectory += log["program_str"] + "\n"
            if log["type"] == "action":
                trajectory += f"Agent performs an action: {log['name']}." + "\n"
            elif log["type"] == "perception":
                trajectory += (
                    f"Agent performs a perception: {log['name']}. The result is {log['result']}."
                    + "\n"
                )
            trajectory += "Partial state:" + "\n"
            trajectory += log["state"] + "\n"

            try:
                if abs(log["instant_reward"]) >= 0.000001:
                    trajectory += (
                        f"The agent got a reward of {log['instant_reward']}\n\n"
                    )
                else:
                    trajectory += "\n"
            except:
                trajectory += "\n"

        if len(logs[1:]) >= max_steps:
            trajectory += f"The total step number is {len(logs[1:])}, the latter ones are truncated."

        user_prompt = (
            REVISION_AGENT_PROGRAM_EXECUTION_TRACE.replace("<<task_name>>", self.task.upper())
            .replace("<<task_map_desc>>", self.task_template.map_desc)
            .replace(
                "<<task_agent_position_desc>>", self.task_template.agent_position_desc
            )
            .replace("<<task_goal_desc>>", self.task_template.goal_desc)
            .replace("<<task_return_desc>>", self.task_template.return_desc)
            .replace("<<initial_state>>", initial_state)
            .replace("<<trajectory>>", trajectory)
            .replace("<<reward>>", str(reward))
            .replace("<<program>>", logs[0]["program_str"])
            .replace("<<average_reward>>", str(average_reward))
        )
        return user_prompt
