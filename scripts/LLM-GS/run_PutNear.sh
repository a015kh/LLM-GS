task="PutNear"
starting_seed=0
interval=8
ending_seed=$(($starting_seed + $interval - 1))
search_space="MinigridProgrammaticSpace"
max_program_nums=10000

for seed in $(seq $starting_seed $ending_seed); do
    python3 scripts/main.py --seed ${seed} --task ${task} --output_name "LLM-GS_Minigrid" --search_space ${search_space} --max_program_nums ${max_program_nums}
done