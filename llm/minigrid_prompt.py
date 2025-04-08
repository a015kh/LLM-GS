from .prompt_template import SystemPromptTemplate, UserPromptTemplate

MINIGRID_ENV_DESC_DSL = """In the Minigrid environment, you navigate a grid-based world referred to as a "map." Within this map, an entity called the "agent" can move, change direction, and interact with objects. The map also includes obstacles like "walls," which block the agent's movement; if the agent encounters a wall, it remains stationary. Another obstacle is "lava," which ends the episode if the agent steps on it. Additionally, there are "doors" that block the agent until opened using the "toggle" action.

At the start of each episode, various objects are scattered across the map, and the agent can interact with them as needed. These objects fall into four categories: "lava," "door," "ball," and "box." Except for lava, objects can appear in two colors: "red" and "blue."

Lava: Ends the episode when stepped on.
Door: Blocks the agent's path until opened using the "toggle" action.
Ball: Can be picked up and dropped.
Box: Can be picked up and dropped.

Your objective is to generate the appropriate Minigrid dsl program based on a given task name and description. This Minigrid dsl program will encompass actions enabling the agent to engage with the environment, alongside perceptions facilitating the agent's recognition of the environment's dynamics.
"""

MINIGRID_ENV_DESC_PYTHON = """In the Minigrid environment, you navigate a grid-based world referred to as a "map." Within this map, an entity called the "agent" can move, change direction, and interact with objects. The map also includes obstacles like "walls," which block the agent's movement; if the agent encounters a wall, it remains stationary. Another obstacle is "lava," which ends the episode if the agent steps on it. Additionally, there are "doors" that block the agent until opened using the "toggle" action.

At the start of each episode, various objects are scattered across the map, and the agent can interact with them as needed. These objects fall into four categories: "lava," "door," "ball," and "box." Except for lava, objects can appear in two colors: "red" and "blue."

Lava: Ends the episode when stepped on.
Door: Blocks the agent's path until opened using the "toggle" action.
Ball: Can be picked up and dropped.
Box: Can be picked up and dropped.

Your objective is to generate the appropriate Python program based on a given task name and description. This Python program will encompass actions enabling the agent to engage with the environment, alongside perceptions facilitating the agent's recognition of the environment's dynamics.
"""

### Action Descriptions

FORWARD_DESC_PYTHON = """forward(): Asks the agent to move forward one cell. The agent will stay still if a wall or an unopened door is blocking its way. The episode will be terminated if the agent steps on lava."""

LEFT_DESC_PYTHON = """left(): Asks the agent to rotate 90 degrees counterclockwise."""

RIGHT_DESC_PYTHON = """right(): Asks the agent to rotate 90 degrees clockwise."""

PICKUP_DESC_PYTHON = """pickup(): Asks the agent to pick up an object right in front of the current cell. The agent can only carry one object at a time."""

DROP_DESC_PYTHON = """drop(): Asks the agent to drop the object it is carrying right in front of the current cell. The agent can only drop the object if it is carrying one and there is no object in the cell."""

TOGGLE_DESC_PYTHON = """toggle(): Asks the agent to change the state of a door directly in front of its current position. The agent can use this action to open or close the door immediately ahead."""


FORWARD_DESC_DSL = """forward: Asks the agent to move forward one cell. The agent will stay still if a wall or an unopened door are blocking its way. The agent will terminate the episode if it steps on lava."""

LEFT_DESC_DSL = """left: Asks the agent to rotate 90 degrees counterclockwise."""

RIGHT_DESC_DSL = """right: Asks the agent to rotate 90 degrees clockwise."""

PICKUP_DESC_DSL = """pickup: Asks the agent to pick up an object right in front of the current cell. The agent can only carry one object at a time."""

DROP_DESC_DSL = """drop: Asks the agent to drop the object it is carrying right in front of the current cell. The agent can only drop the object if it is carrying one and there is no object in the cell."""

TOGGLE_DESC_DSL = """toggle: Asks the agent to change the state of a door directly in front of its current position. The agent can use this action to open or close the door immediately ahead."""

MINIGRID_ACTION_DESC_LIST_PYTHON = [
    FORWARD_DESC_PYTHON,
    LEFT_DESC_PYTHON,
    RIGHT_DESC_PYTHON,
    PICKUP_DESC_PYTHON,
    DROP_DESC_PYTHON,
    TOGGLE_DESC_PYTHON,
]

MINIGRID_ACTION_DESC_LIST_DSL = [
    FORWARD_DESC_DSL,
    LEFT_DESC_DSL,
    RIGHT_DESC_DSL,
    PICKUP_DESC_DSL,
    DROP_DESC_DSL,
    TOGGLE_DESC_DSL,
]

### Perception Descriptions

FRONT_IS_CLEAR_DESC_PYTHON = """front_is_clear(): Returns True if there is no wall and an unopened door right in front of the agent. It can only check wall and unopened door, so if there is lava right in front of the agent, it will return True."""

FRONT_OBJECT_TYPE_DESC_PYTHON = """front_object_type(type: str): Returns True if there is an object of the specified type right in front of the agent. The type can be and only can be "lava", "door", "ball", or "box"."""

FRONT_OBJECT_COLOR_DESC_PYTHON = """front_object_color(color: str): Returns True if there is an object of the specified color right in front of the agent. The color can be and only can be "red" or "blue"."""

IS_CARRYING_OBJECT_DESC_PYTHON = (
    """is_carrying_object(): Returns True if the agent is carrying an object."""
)


FRONT_IS_CLEAR_DESC_DSL = """front_is_clear: Returns True if there is no wall and an unopened door right in front of the agent. Notice that the lava can be stepped on so it will return True if there is lava right in front of the agent."""

FRONT_OBJECT_TYPE_DESC_DSL = """front_object_type(type): Returns True if there is an object of the specified type right in front of the agent. The type can be and only can be "lava", "door", "ball", or "box"."""

FRONT_OBJECT_COLOR_DESC_DSL = """front_object_color(color): Returns True if there is an object of the specified color right in front of the agent. The color can be and only can be "red" or "blue"."""

IS_CARRYING_OBJECT_DESC_DSL = (
    """is_carrying_object: Returns True if the agent is carrying an object."""
)

MINIGRID_PERCEPTION_DESC_LIST_PYTHON = [
    FRONT_IS_CLEAR_DESC_PYTHON,
    FRONT_OBJECT_TYPE_DESC_PYTHON,
    FRONT_OBJECT_COLOR_DESC_PYTHON,
    IS_CARRYING_OBJECT_DESC_PYTHON,
]

MINIGRID_PERCEPTION_DESC_LIST_DSL = [
    FRONT_IS_CLEAR_DESC_DSL,
    FRONT_OBJECT_TYPE_DESC_DSL,
    FRONT_OBJECT_COLOR_DESC_DSL,
    IS_CARRYING_OBJECT_DESC_DSL,
]

### Perception Descriptions

MINIGRID_DSL_DESC = """This is the production role of the domain-specific language of the Karel environment.
Program p := DEF run m( s m)
Statement s := WHILE c( b c) w( s w) | IF c( b c) i( s i) | IFELSE c( b c) i( s i) ELSE e( s e) | REPEAT R=n r( s r) | s s | a
Condition b := h | not c( h c)
Number n := 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19
Perception h := front_is_clear | front_object_type h( type h) | front_object_color h( color h) | is_carrying_object
Action a := forward | left | right | pickup | drop | toggle
Type t := lava | door | ball | box
Color c := red | blue
"""

PYTHON_TO_MINIGRID = """Python to Minigrid dsl conversion
1. "def run(): s" to "DEF run m( s m)"
2. "while b: s" to "WHILE c( b c) w( s w)"
3. "if b: s" to "IF c( b c) i( s i)"
4. "if b: s else: s" to "IFELSE c( b c) i( s i) ELSE e( s e)"
5. "for i in range(n): s" to "REPEAT R=n r( s r)"
6. "not h" to "not c( h c)"
7. "front_is_clear()" to "front_is_clear"
8. "front_object_type(type)" to "front_object_type h( type h)"
9. "front_object_color(color)" to "front_object_color h( color h)"
10. "is_carrying_object()" to "is_carrying_object"
11. "forward()" to "forward"
12. "left()" to "left"
13. "right()" to "right"
14. "pickup()" to "pickup"
15. "drop()" to "drop"
16. "toggle()" to "toggle"
"""


MINIGRID_TASK_MAP_DESC = {
    "LavaGap": "The map is a 6x6 grid surrounded by walls. There is a vertical strip of lava with a randomly selected gap in the middle of the map and a goal square at the bottom right corner.",
    "PutNear": "The map is a 6x6 grid surrounded by walls. There are two objects, one is a ball and the other is a box. The two objects are randomly placed on the map.",
    "RedBlueDoor": "The map is a 6x12 grid surrounded by walls that are vertically split into three chambers. The left chamber is a 4x2 grid, the middle chamber is a 4x4 grid and the right chamber is a 4x2 grid. On the wall between the left and middle chamber, there is a randomly placed red door. On the wall between the middle and right chamber, there is a randomly placed blue door.",
}

MINIGRID_TASK_AGENT_POSITION_DESC = {
    "LavaGap": "The agent starts at the top left corner of the map facing east.",
    "PutNear": "The agents start at a random position with a random direction in the map.",
    "RedBlueDoor": "The agent starts at a random position with a random direction in the middle chamber.",
}

MINIGRID_TASK_GOAL_DESC = {
    "LavaGap": "The agent has to reach the goal square at the bottom right corner of the map without step on lava. Touching the lava terminates the episode.",
    "PutNear": "The agent has to first locate and pick up the ball. Next, it needs to find the box and drop the ball either to the right or left of it. Picking up the wrong object will terminate the episode.",
    "RedBlueDoor": "The agent has to first find and open the red door, then find and open the blue door. Opening the blue door first will terminate the episode.",
}

MINIGRID_TASK_RETURN_DESC = {
    "LavaGap": "If the agent reaches the goal, it will receive a reward of 1. If the agent steps on lava, it will receive a reward of -1.",
    "PutNear": "If the agent picks up the ball, it will receive a reward of 0.5. If the agent drops the ball to the right or the left of the box, it will receive a reward of 1. If the agent picks up the wrong object, it will receive a reward of -1.",
    "RedBlueDoor": "If the agent opens the red door first, it will receive a reward of 0.5. If the agent opens the blue door after opening the red door, it will receive a reward of 0.5. If the agent opens the blue door first, it will receive a reward of -1.",
}


class MinigridPythonPromptTemplate(SystemPromptTemplate):
    def __init__(self):
        super().__init__("minigrid", "python")

    ## System Prompt ###
    @property
    def env_desc(self) -> str:
        return MINIGRID_ENV_DESC_PYTHON

    @property
    def action_desc(self) -> str:
        action_desc_str = "Here are the available actions for the agent:\n"
        action_desc_str += "\n".join(MINIGRID_ACTION_DESC_LIST_PYTHON) + "\n"
        return action_desc_str

    @property
    def perception_desc(self) -> str:
        perception_desc_str = "Here are the available perceptions of the agent:\n"
        perception_desc_str += "\n".join(MINIGRID_PERCEPTION_DESC_LIST_PYTHON) + "\n"
        return perception_desc_str

    @property
    def python_to_dsl(self) -> str:
        return PYTHON_TO_MINIGRID


class MinigridDSLPromptTemplate(SystemPromptTemplate):
    def __init__(self):
        super().__init__("minigrid", "dsl")

    ## System Prompt ###
    @property
    def env_desc(self) -> str:
        return MINIGRID_ENV_DESC_DSL

    @property
    def action_desc(self) -> str:
        action_desc_str = "Here are the available actions for the agent:\n"
        action_desc_str += "\n".join(MINIGRID_ACTION_DESC_LIST_DSL) + "\n"
        return action_desc_str

    @property
    def perception_desc(self) -> str:
        perception_desc_str = "Here are the available perceptions of the agent:\n"
        perception_desc_str += "\n".join(MINIGRID_PERCEPTION_DESC_LIST_DSL) + "\n"
        return perception_desc_str

    @property
    def dsl_desc(self) -> str:
        return MINIGRID_DSL_DESC


class MinigridUserPrompt(UserPromptTemplate):
    def __init__(self, task: str):
        super().__init__(task)
        self.task = task
        self.map_desc = MINIGRID_TASK_MAP_DESC[task]
        self.agent_position_desc = MINIGRID_TASK_AGENT_POSITION_DESC[task]
        self.goal_desc = MINIGRID_TASK_GOAL_DESC[task]
        self.return_desc = MINIGRID_TASK_RETURN_DESC[task]

    ### User Prompt ###
    @property
    def task_map_desc(self) -> str:
        return self.map_desc

    @property
    def task_agent_position_desc(self) -> str:
        return self.agent_position_desc

    @property
    def task_goal_desc(self) -> str:
        return self.goal_desc

    @property
    def task_return_desc(self) -> str:
        return self.return_desc
