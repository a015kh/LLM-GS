task="CleanHouse"
search_method="HillClimbing"
search_space="ProgrammaticSpace"
k=250
starting_seed=0
interval=32
ending_seed=$(($starting_seed + $interval - 1))

for seed in $(seq $starting_seed $ending_seed); do
    python3 scripts/baseline.py --seed ${seed} --task ${task} --output_name "HC" --search_method $search_method --k $k --search_space $search_space
done