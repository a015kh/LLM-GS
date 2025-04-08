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
