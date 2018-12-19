url=http://localhost:9027/audioclips/search?pattern=
# url=https://m2.audiocommons.org/api/audioclips/search?pattern=
## declare an array variable
declare -a arr=("dog" "cat" "fish" "bird" "love" "dance" "bamos" "ciao" "ptica" "privet" "food" "bamboo" "flower" "deep" "clear" "rain" "sun" "peace" "mission" "chance")

for i in "${arr[@]}"
do
    echo "$i"
    curl -v -H "Content-Type: application/json" -X GET {$url}{$i} &
    # sleep 1
done