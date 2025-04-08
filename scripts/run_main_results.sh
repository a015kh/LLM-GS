method="LLM-GS"
task="CleanHouse"

# LLM-GS (Karel): CleanHouse, DoorKey, FourCorners, Harvester, MazeSparse, OneStroke, PathFollow, Seeder, Snake, StairClimberSparse, TopOff, WallAvoider
# LLM-GS (Minigrid): LavaGap, PutNear, RedBlueDoor
# HC (Karel): CleanHouse, DoorKey, FourCorners, Harvester, MazeSparse, OneStroke, PathFollow, Seeder, Snake, StairClimberSparse, TopOff, WallAvoider
# HC (Minigrid): LavaGap, PutNear, RedBlueDoor
# CEBS: CleanHouse, DoorKey, FourCorners, Harvester, MazeSparse, OneStroke, Seeder, Snake, StairClimberSparse, TopOff
# LEAPS: CleanHouse, DoorKey, FourCorners, Harvester, MazeSparse, OneStroke, Seeder, Snake, StairClimberSparse, TopOff

source scripts/$method/run_$task.sh