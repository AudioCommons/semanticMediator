## declare an array variable
declare -a arr=("dog" "cat" "fish" "bird" "love" "dance" "bamos" "ciao" "ptica" "privet")

for i in "${arr[@]}"
do
    echo "$i"
    curl -v -H "Content-Type: application/json" -X GET http://localhost:9027/audioclips/search?pattern={$i} &
    # sleep 1
done  