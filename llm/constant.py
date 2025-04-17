PYTHON_LIMITATION = \
"""There are some limitations for the Python program:
- do not define other functions besides run()
- do not call other functions
- do not define variables
- do not use True, False, break, continue, return, ==, !=, elif, or, and
"""

USER_PROMPT_TEMPLATE_PYTHON_TO_DSL = \
"""I'll provide you with the task name and description.

Task name: <<task_name>>
Task map: <<task_map_desc>>
Task agent position: <<task_agent_position_desc>>
Task goal: <<task_goal_desc>>
Task return: <<task_return_desc>>

1. Generate 1 simple and short Python program to tackle the task, avoid using comments.
2. Convert the Python program to the <<environment_name>> dsl program."""

USER_PROMPT_TEMPLATE_PYTHON = \
"""I'll provide you with the task name and description.

Task name: <<task_name>>
Task map: <<task_map_desc>>
Task agent position: <<task_agent_position_desc>>
Task goal: <<task_goal_desc>>
Task return: <<task_return_desc>>

1. Generate 1 simple and short Python program to tackle the task, avoid using comments."""

USER_PROMPT_TEMPLATE_DSL = \
"""I'll provide you with the task name and description.

Task name: <<task_name>>
Task map: <<task_map_desc>>
Task agent position: <<task_agent_position_desc>>
Task goal: <<task_goal_desc>>
Task return: <<task_return_desc>>

1. Generate 1 simple and short <<environment_name>> dsl program to tackle the task, avoid using comments."""

REVISION_REGENERATION_WITH_REWARD = \
"""I'll provide you with the task name, task description, and the programs rewards pairs sorted by their evaluation rewards from 32 task variants.

Task name: <<task_name>>
Task map: <<task_map_desc>>
Task agent position: <<task_agent_position_desc>>
Task goal: <<task_goal_desc>>
Task return: <<task_return_desc>>

Program reward pairs sorted by their evaluation rewards:
<<programs>>
1. Depending on this information, examine the program pattern that the highest score programs process, but the lowest score programs do not.
2. Generate 1 simple and short Python program according to the pattern to tackle the task, avoid using comment.
3. Convert the Python program to the Karel dsl program.
"""

REVISION_REGENERATION = \
"""I'll provide you with the task name, task description, and the programs you generated last time.

Task name: <<task_name>>
Task map: <<task_map_desc>>
Task agent position: <<task_agent_position_desc>>
Task goal: <<task_goal_desc>>
Task return: <<task_return_desc>>

These are the programs you generated last time, all of these programs cannot yield perfect performance.

<<programs>>
1. Generate a Python program that is not identical to any of the previous programs to tackle the task, and avoid using comments.
2. Convert the Python program to the Karel dsl program."""

REVISION_AGENT_EXECUTION_TRACE = \
"""I'll provide you with the code you developed previously, with the goal of refining it. To guide your revision, you'll receive the specific task name and a description. Since there are 32 different versions of the task that share the same objective but differ by random seeds, I will identify the specific variant where the performance of the program is most lacking. Additionally, you'll get the initial state of the task, the code, and a detailed trajectory demonstrating how the code operates within this particular scenario. This trajectory will detail each action step-by-step and show a localized snapshot of the environment (a 3x3 area centered on the agent) during execution. Rewards received by the agent will also be shown during these steps.

Task name: <<task_name>>
Task map: <<task_map_desc>>
Task agent position: <<task_agent_position_desc>>
Task goal: <<task_goal_desc>>
Task return: <<task_return_desc>>

Initial state:
<<initial_state>>

Program:
<<program>>

The average reward on 32 task variants is:
<<average_reward>>

Trajectory:

<<trajectory>>

The total reward is <<reward>>

1. Depending on this information, please analyze the reason why the program failed to achieve 1.0 on this task variant and generate a new strategy to solve this task.
2. Generate 1 simple and short Python program according to the new strategy to tackle the task, avoid using comment.
3. Convert the Python program to the Karel dsl program.
"""

REVISION_AGENT_PROGRAM_EXECUTION_TRACE = \
"""I'll provide you with the code you developed previously, with the goal of refining it. To guide your revision, you'll receive the specific task name and a description. Since there are 32 different versions of the task that share the same objective but differ by random seeds, I will identify the specific variant where the performance of the program is most lacking. Additionally, you'll get the initial state of the task, the code, and a detailed trajectory demonstrating how the code operates within this particular scenario. This trajectory will detail each action step-by-step, indicate which section of your code is active, and show a localized snapshot of the environment (a 3x3 area centered on the agent) during execution. Rewards received by the agent will also be shown during these steps.

Task name: <<task_name>>
Task map: <<task_map_desc>>
Task agent position: <<task_agent_position_desc>>
Task goal: <<task_goal_desc>>
Task return: <<task_return_desc>>

Initial state:
<<initial_state>>

Program:
<<program>>

The average reward on 32 task variants is:
<<average_reward>>

Trajectory:

<<trajectory>>

The total reward is <<reward>>

1. Depending on this information, please analyze the reason why the program failed to achieve 1.0 on this task variant and generate a new strategy to solve this task.
2. Generate 1 simple and short Python program according to the new strategy to tackle the task, avoid using comment.
3. Convert the Python program to the Karel dsl program.
"""