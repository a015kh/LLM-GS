task="PathFollow"
search_method="Scheduled_HillClimbing"
search_space="ProgrammaticSpace"
start_k=32
end_k=2048
starting_seed=0
interval=32
ending_seed=$(($starting_seed + $interval - 1))

for seed in $(seq $starting_seed $ending_seed); do
    python3 scripts/main.py --seed ${seed} --task ${task} --start_k ${start_k} --end_k ${end_k} --output_name "LLM-GS" --search_method ${search_method} --search_space ${search_space}
done