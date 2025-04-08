from .prompt_template import SystemPromptTemplate, UserPromptTemplate


KAREL_ENV_DESC_PYTHON = \
"""You're currently navigating within a Karel environment, which is essentially a grid world. In this context, a "world" is referred to as a "map." Within this map, there's an entity known as the "agent," capable of movement, changing direction, as well as picking up and placing markers on the map. Additionally, there are obstacles called "walls" that impede the agent's progress; whenever the agent encounters a wall, it turns around. Furthermore, there are pre-existing "markers" scattered throughout the map at the beginning, though the agent has the ability to both pickup and place these markers as needed.

Your objective is to generate the appropriate Python program based on a given task name and description. This Python program will encompass actions enabling the agent to engage with the environment, alongside perceptions facilitating the agent's recognition of the environment's dynamics.
"""

KAREL_ENV_DESC_DSL= \
"""You're currently navigating within a Karel environment, which is essentially a grid world. In this context, a "world" is referred to as a "map." Within this map, there's an entity known as the "agent," capable of movement, changing direction, as well as picking up and placing markers on the map. Additionally, there are obstacles called "walls" that impede the agent's progress; whenever the agent encounters a wall, it turns around. Furthermore, there are pre-existing "markers" scattered throughout the map at the beginning, though the agent has the ability to both pickup and place these markers as needed.

Your objective is to generate the appropriate Karel dsl program based on a given task name and description. This Karel dsl program will encompass actions enabling the agent to engage with the environment, alongside perceptions facilitating the agent's recognition of the environment's dynamics.
"""

### Action Descriptions

MOVE_DESC_PYTHON = \
"""move(): Asks the agent to move forward one cell. The agent will instead turn left twice if a wall is blocking its way."""

TURN_LEFT_DESC_PYTHON = \
"""turnLeft(): Asks the agent to rotate 90 degrees counterclockwise."""

TURN_RIGHT_DESC_PYTHON = \
"""turnRight(): Asks the agent to rotate 90 degrees clockwise."""

PICK_MARKER_DESC_PYTHON = \
"""pickMarker(): Asks the agent to pick up one marker from the current cell."""

PUT_MARKER_DESC_PYTHON = \
"""putMarker(): Asks the agent to put down one marker on the current cell."""

MOVE_DESC_DSL = \
"""move: Asks the agent to move forward one cell. The agent will instead turn left twice if a wall is blocking its way."""

TURN_LEFT_DESC_DSL = \
"""turnLeft: Asks the agent to rotate 90 degrees counterclockwise."""

TURN_RIGHT_DESC_DSL = \
"""turnRight: Asks the agent to rotate 90 degrees clockwise."""

PICK_MARKER_DESC_DSL = \
"""pickMarker: Asks the agent to pick up one marker from the current cell."""

PUT_MARKER_DESC_DSL = \
"""putMarker: Asks the agent to put down one marker on the current cell."""

KAREL_ACTION_DESC_LIST_PYTHON = [MOVE_DESC_PYTHON, TURN_LEFT_DESC_PYTHON, TURN_RIGHT_DESC_PYTHON, PICK_MARKER_DESC_PYTHON, PUT_MARKER_DESC_PYTHON]

KAREL_ACTION_DESC_LIST_DSL = [MOVE_DESC_DSL, TURN_LEFT_DESC_DSL, TURN_RIGHT_DESC_DSL, PICK_MARKER_DESC_DSL, PUT_MARKER_DESC_DSL]

### Action Descriptions

### Perception Descriptions

FRONT_IS_CLEAR_DESC_PYTHON = \
"""frontIsClear(): Returns True if there is no wall in front of the agent."""

LEFT_IS_CLEAR_DESC_PYTHON = \
"""leftIsClear(): Returns True if there is no wall on the agent's left."""

RIGHT_IS_CLEAR_DESC_PYTHON = \
"""rightIsClear(): Returns True if there is no wall on the agent's right."""

MARKERS_PRESENT_DESC_PYTHON = \
"""markersPresent(): Returns True if there exist markers on the current cell."""

NO_MARKERS_PRESENT_DESC_PYTHON = \
"""noMarkersPresent(): Returns True if there is no marker on the current cell."""

FRONT_IS_CLEAR_DESC_DSL = \
"""frontIsClear: Returns True if there is no wall in front of the agent."""

LEFT_IS_CLEAR_DESC_DSL = \
"""leftIsClear: Returns True if there is no wall on the agent's left."""

RIGHT_IS_CLEAR_DESC_DSL = \
"""rightIsClear: Returns True if there is no wall on the agent's right."""

MARKERS_PRESENT_DESC_DSL = \
"""markersPresent: Returns True if there exist markers on the current cell."""

NO_MARKERS_PRESENT_DESC_DSL = \
"""noMarkersPresent: Returns True if there is no marker on the current cell."""

KAREL_PERCEPTION_DESC_LIST_PYTHON = [FRONT_IS_CLEAR_DESC_PYTHON, LEFT_IS_CLEAR_DESC_PYTHON, RIGHT_IS_CLEAR_DESC_PYTHON, MARKERS_PRESENT_DESC_PYTHON, NO_MARKERS_PRESENT_DESC_PYTHON]

KAREL_PERCEPTION_DESC_LIST_DSL = [FRONT_IS_CLEAR_DESC_DSL, LEFT_IS_CLEAR_DESC_DSL, RIGHT_IS_CLEAR_DESC_DSL, MARKERS_PRESENT_DESC_DSL, NO_MARKERS_PRESENT_DESC_DSL]

### Perception Descriptions

KAREL_DSL_DESC = \
"""This is the production role of the domain-specific language of the Karel environment.
Program p := DEF run m( s m)
Statement s := WHILE c( b c) w( s w) | IF c( b c) i( s i) | IFELSE c( b c) i( s i) ELSE e( s e) | REPEAT R=n r( s r) | s s | a
Condition b := h | not c( h c)
Number n := 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19
Perception h := frontIsClear | leftIsClear | rightIsClear | markersPresent | noMarkersPresent
Action a := move | turnLeft | turnRight | putMarker | pickMarker
"""

PYTHON_TO_KAREL = \
"""Python to Karel dsl conversion
1. "def run(): s" to "DEF run m( s m)"
2. "while b: s" to "WHILE c( b c) w( s w)"
3. "if b: s" to "IF c( b c) i( s i)"
4. "if b: s else: s" to "IFELSE c( b c) i( s i) ELSE e( s e)"
5. "for i in range(n): s" to "REPEAT R=n r( s r)"
6. "not h" to "not c( h c)"
7. "frontIsClear()" to "frontIsClear"
8. "leftIsClear()" to "leftIsClear"
9. "rightIsClear()" to "rightIsClear"
10. "markersPresent()" to "markersPresent"
11. "noMarkersPresent()" to "noMarkersPresent"
12. "move()" to "move"
13. "turnLeft()" to "turnLeft"
14. "turnRight()" to "turnRight"
15. "putMarker()" to "putMarker"
16. "pickMarker()" to "pickMarker"
"""

KAREL_TASK_MAP_DESC = {
    "StairClimberSparse": "The map is a 12x12 grid surrounded by walls with stairs formed by walls and a marker is randomly initialized on the stairs as a goal.",
    "MazeSparse": "The map is a complex 8x8 grid surrounded by walls and a random marker is placed on an empty cell as a goal.",
    "FourCorners": "The map is an empty 12x12 grid surrounded by walls.",
    "TopOff": "The map is a 12x12 grid surrounded by walls with markers randomly placed on the bottom row of the map.",
    "Harvester": "The map is a 8x8 grid surrounded by walls that starts with a marker on each cell.",
    "CleanHouse": "The map is a complex 14x22 grid made of many connected rooms and is surrounded by walls. There are ten markers randomly placed adjacent to the walls.",
    "DoorKey": "The map is a 8x8 grid surrounded by walls that is vertically split into two chambers. The left chamber is 6x3 grid and the right chamber is 6x2 grid. There is a marker placed randomly on the left chamber as a key, and another marker placed randomly on the right chamber as a goal.",
    "OneStroke": "The map is given by an empty 8x8 grid surrounded by walls.",
    "Seeder": "The map is given by an empty 8x8 grid surrounded by walls.",
    "Snake": "The map is given by an empty 8x8 grid surrounded by walls with a marker randomly placed on the map.",
    "PathFollow": "The map is given by a 8x8 grid surrounded by walls. There is a rugged ascending markers line that starts from the bottom left cell and randomly grows either north or to the east until it reaches the top right cell. Resulting in a rugged markers line connecting the bottom left cell and the top right cell.",
    "WallAvoider": "The map is given by an empty 8x5 grid surrounded by walls."
}

KAREL_TASK_AGENT_POSITION_DESC = {
    "StairClimberSparse": "The agent starts on a random position on the stairs facing east.",
    "MazeSparse": "The agent starts on a random empty cell of the map facing east.",
    "FourCorners": "The agent starts on a random cell on the bottom row of the map facing east.",
    "TopOff": "The agent starts on the bottom left cell of the map facing east.",
    "Harvester": "The agent starts on a random cell on the bottom row of the map facing east.",
    "CleanHouse": "The agent starts on a fixed cell facing south.",
    "DoorKey": "The agent starts on a random cell on the left chamber facing east.",
    "OneStroke": "The agent starts on a random cell of the map facing east.",
    "Seeder": "The agent starts on a random cell of the map facing east.",
    "Snake": "The agent starts on a random cell of the map facing east.",
    "PathFollow": "The agent starts on the bottom left cell of the map facing north.",
    "WallAvoider": "The agent starts on a random cell of the map facing random directions."
}

KAREL_TASK_GOAL_DESC = {
    "StairClimberSparse": "The goal of the agent is to reach a marker that is also randomly initialized on the stairs.",
    "MazeSparse": "The goal of the agent is to reach the goal marker.",
    "FourCorners": "The goal of the agent is to place one marker in each corner of the map.",
    "TopOff": "The goal of the agent is to place one extra marker on top of every marker on the map.",
    "Harvester": "The goal of the agent is to pick up every marker on the map.",
    "CleanHouse": "The goal of the agent is to pick up every marker on the map.",
    "DoorKey": "The goal of the agent is to pick up a marker on the left chamber, which opens a door connecting both chambers. Allow the agent to reach and put a marker on the goal marker.",
    "OneStroke": "The goal of the agent is to visit every grid cell without repeating. Visited cells become a wall that terminates the episode upon touching.",
    "Seeder": "The goal of the agent is to place one marker in every empty cell of the map.",
    "Snake": "The agent acts like the head of a snake, whose body grows each time a marker is reached. (No need to pick it up.) Every time a marker is reached, the body of the agent grows one marker. The goal of the agent is to touch the marker on the map without colliding with the snake's body, which terminates the episode. Each time the marker is reached, it is placed on a random cell, until 20 markers are reached.",
    "PathFollow": "The goal of the agent is to collect every marker on that rugged markers line without leaving the rugged markers line two cells away.",
    "WallAvoider": "The goal of the agent is to place exactly one marker in every interior cell of the map, which refers to the cells that are not adjacent to any wall."
}

KAREL_TASK_RETURN_DESC = {
    "StairClimberSparse": "If the agent reaches the marker, the agent receives 1 as an episodic return and 0 otherwise. If the agent moves to an invalid position, i.e. outside the contour of the stairs, the episode terminates with a -1 return.",
    "MazeSparse": "If the agent reaches the marker, the agent receives 1 as an episodic return and 0 otherwise.",
    "FourCorners": "Return is given by the number of corners with one marker divided by 4.",
    "TopOff": "Return is given by the number of markers that have been topped off divided by the total number of markers. Picking up the marker will terminate the episode with a -1 return.",
    "Harvester": "Return is given by the number of picked-up markers divided by the total number of markers.",
    "CleanHouse": "Return is given by the number of picked-up markers divided by the total number of markers.",
    "DoorKey": "Picking up the first marker yields a 0.5 reward, and putting a marker on the goal marker yields an additional 0.5.",
    "OneStroke": "Return is given by the number of visited cells divided by the total number of empty cells in the initial state.",
    "Seeder": "Return is given by the number of cells with one marker divided by the total number of empty cells in the initial state.",
    "Snake": " Return is given by the number of reached markers divided by 20.",
    "PathFollow": "Return is given by the number of picked-up markers divided by the total number of markers. Placing any marker or leaving the rugged markers line two cells away will have a negative return as -1.0 and terminate the episode.",
    "WallAvoider": "Return is given by the number of interior cells with exactly one marker divided by the total number of interior cells. Picking up the marker, putting more than one marker on one cell, or putting any marker on the cell adjacent to any wall will terminate the episode with a -1 return."
}

class KarelPythonPromptTemplate(SystemPromptTemplate):
    def __init__(self) -> None:
        super().__init__("karel", "python")

    ### System Prompt ###
    @property
    def env_desc(self) -> str:
        return KAREL_ENV_DESC_PYTHON
    
    @property
    def action_desc(self) -> str:
        action_desc_str = "Here are the available actions for the agent:\n"
        action_desc_str += "\n".join(KAREL_ACTION_DESC_LIST_PYTHON) + "\n"
        return action_desc_str
    
    @property
    def perception_desc(self) -> str:
        perception_desc_str = "Here are the available perceptions of the agent:\n"
        perception_desc_str += "\n".join(KAREL_PERCEPTION_DESC_LIST_PYTHON) + "\n"
        return perception_desc_str
    
    @property
    def python_to_dsl(self) -> str:
        return PYTHON_TO_KAREL


class KarelDSLPromptTemplate(SystemPromptTemplate):
    def __init__(self) -> None:
        super().__init__("karel", "dsl")
        
    ### System Prompt ###
    @property
    def env_desc(self) -> str:
        return KAREL_ENV_DESC_DSL
    
    @property
    def action_desc(self) -> str:
        action_desc_str = "Here are the available actions for the agent:\n"
        action_desc_str += "\n".join(KAREL_ACTION_DESC_LIST_DSL) + "\n"
        return action_desc_str
    
    @property
    def perception_desc(self) -> str:
        perception_desc_str = "Here are the available perceptions of the agent:\n"
        perception_desc_str += "\n".join(KAREL_PERCEPTION_DESC_LIST_DSL) + "\n"
        return perception_desc_str
    
    @property
    def dsl_desc(self) -> str:
        return KAREL_DSL_DESC

    
class KarelUserPrompt(UserPromptTemplate):
    def __init__(
        self,
        task: str,
    ) -> None:
        super().__init__(task)
        self.map_desc = KAREL_TASK_MAP_DESC[self.task]
        self.agent_position_desc = KAREL_TASK_AGENT_POSITION_DESC[self.task]
        self.goal_desc = KAREL_TASK_GOAL_DESC[self.task]
        self.return_desc = KAREL_TASK_RETURN_DESC[self.task]

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
