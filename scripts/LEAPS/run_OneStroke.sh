task="OneStroke"
search_method="CEM"
search_space="LatentSpace"
k=64
e=3
sigma=0.5
starting_seed=0
interval=5
ending_seed=$(($starting_seed + $interval - 1))

for seed in $(seq $starting_seed $ending_seed); do
    python3 scripts/baseline.py --seed ${seed} --task ${task} --output_name "LEAPS" --search_method $search_method --k $k --es $e --search_space $search_space --sigma $sigma
done
