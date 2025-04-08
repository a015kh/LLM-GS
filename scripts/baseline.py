import sys
import pathlib
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

sys.path.append(".")
sys.path.append("./leaps")

from prog_policies.utils import get_env_name
from prog_policies.karel import KarelDSL
from prog_policies.karel_tasks import get_task_cls as get_karel_task_cls
from prog_policies.minigrid.dsl import MinigridDSL
from prog_policies.minigrid_tasks import get_task_cls as get_minigrid_task_cls
from prog_policies.search_space import get_search_space_cls
from prog_policies.search_methods import get_search_method_cls
from prog_policies.utils.evaluate_and_search import check_save_time, record_search
from prog_policies.utils.save_file import inside_seed_save_log_file, outside_seed_save_log_file

import time
import os

def karel_env(args):
    dsl = KarelDSL()

    env_args = {
        "env_height": 8,
        "env_width": 8,
        "crashable": args.crashable,
        "leaps_behaviour": True,
        "max_calls": 10000,
    }

    if (
        args.task == "StairClimber"
        or args.task == "StairClimberSparse"
        or args.task == "TopOff"
        or args.task == "FourCorners"
    ):
        env_args["env_height"] = 12
        env_args["env_width"] = 12

    if args.task == "CleanHouse":
        env_args["env_height"] = 14
        env_args["env_width"] = 22

    if args.task == "WallAvoider":
        env_args["env_height"] = 8
        env_args["env_width"] = 5

    task_cls = get_karel_task_cls(args.task)
    task_envs = [task_cls(env_args, i) for i in range(args.num_envs)]
    return task_envs, dsl


def minigrid_env(args):
    dsl = MinigridDSL()
    task_cls = get_minigrid_task_cls(args.task)
    task_envs = [
        task_cls(i, args.crashable, args.crash_penalty, args.max_calls)
        for i in range(args.num_envs)
    ]
    return task_envs, dsl

if __name__ == "__main__":

    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    
    # LatentSpace, ProgrammaticSpace
    parser.add_argument("--search_space", default="ProgrammaticSpace", help="Search space class name")
    # Scheduled_HillClimbing, HillClimbing, HillClimbingLatent, CEM, CEBS
    parser.add_argument("--search_method", default="HillClimbing", help="Search method class name")
    parser.add_argument("--seed", type=int, default=0, help="Random seed for searching")
    parser.add_argument("--num_envs", type=int, default=32, help="Number of environments to search")
    # Karel: StairClimberSparse, MazeSparse, FourCorners, TopOff, Harvester, CleanHouse
    # Karel-Hard: DoorKey, OneStroke, Seeder, Snake
    # Karel-New: PathFollow, WallAvoider
    # Minigrid: LavaGap, PutNear, RedBlueDoor
    parser.add_argument("--task", default="Seeder", help="Task class name")
    parser.add_argument("--crashable", action="store_true", help="Determine whether the env will terimate upon executing invalid actions")
    parser.add_argument("--crash_penalty", type=float, default=-0.0, help="Penalty for crashing")
    parser.add_argument("--max_calls", type=int, default=1000, help="Max calls for each program")
    parser.add_argument("--sigma", type=float, default=0.1, help="Standard deviation for Gaussian noise in Latent Space")
    parser.add_argument("--k", type=int, default=1024, help="Number of neighbors to consider")
    parser.add_argument("--es", type=int, default=2, help="Number of elite candidates in CEM-based methods")
    parser.add_argument("--max_program_nums", type=int, default=1000000)
    
    parser.add_argument("--output_dir", type=str, default="output")
    parser.add_argument("--output_name", type=str, default="0")
    parser.add_argument("--save_step", type=int, default=5000)
    # parser.add_argument("--output_name", type=str, default="output.json")

    args = parser.parse_args()
    args.e = args.es
    
    print(vars(args))
    
    output_dir = os.path.join(args.output_dir, args.task, args.output_name)
    output_dir_seed = os.path.join(output_dir, str(args.seed))
    
    if os.path.isdir(output_dir_seed):
        assert 0, "Duplicated seed."
    
    pathlib.Path(output_dir_seed).mkdir(parents=True, exist_ok=True)

    if get_env_name(args.task) == "karel":
        task_envs, dsl = karel_env(args)
    elif get_env_name(args.task) == "minigrid":
        task_envs, dsl = minigrid_env(args)
    else:
        assert 0, "Invalid task name."

    search_space_cls = get_search_space_cls(args.search_space)
    search_space = search_space_cls(dsl, args.sigma)
    search_space.set_seed(args.seed)

    search_method_cls = get_search_method_cls(args.search_method)
    if args.search_method == "Scheduled_HillClimbing":
        search_method = search_method_cls(args.k, args.e, args.start_k, args.end_k, args.max_program_nums)
    else:
        search_method = search_method_cls(args.k, args.e)

    best_reward = -float("inf")
    best_prog = None
    
    log = {}
    log['args'] = vars(args)
    log['seed'] = args.seed

    init_time = time.time()

    previous_save_program_num = 0

    while task_envs[0].program_num < args.max_program_nums and best_reward < 1:
        previous_save_program_num = check_save_time(best_prog, best_reward, args.save_step, previous_save_program_num, search_method, task_envs, dsl, output_dir_seed, log, init_time, output_dir, args.task, args.seed)
        best_prog, best_reward, _ = record_search(best_prog, best_reward, search_method, search_space, task_envs, dsl, output_dir_seed, log, init_time, output_dir, args.task, args.seed)

        if best_reward >= 1:
            break

    search_method.record[task_envs[0].program_num] = best_reward
    search_method.program_record[task_envs[0].program_num] = dsl.parse_node_to_str(best_prog)

    inside_seed_save_log_file(log, output_dir_seed, task_envs[0].program_num, init_time, dsl.parse_node_to_str(best_prog), best_reward, search_method.record, search_method.program_record)
    outside_seed_save_log_file(output_dir, args.task, args.seed, task_envs[0].program_num, init_time, dsl.parse_node_to_str(best_prog), best_reward, search_method.record, search_method.program_record)