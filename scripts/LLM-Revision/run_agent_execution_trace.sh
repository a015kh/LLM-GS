task="DoorKey"
starting_seed=0
interval=5
ending_seed=$(($starting_seed + $interval - 1))
revision_method="agent_execution_trace"

for seed in $(seq $starting_seed $ending_seed); do
    python3 scripts/revision.py --task ${task} --output_name $revision_method --revision_method $revision_method --seed ${seed}
done