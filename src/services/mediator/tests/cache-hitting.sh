# url=http://localhost:9027/audioclips/search?pattern=dog
url=https://m2.audiocommons.org/api/audioclips/search?pattern=dog

curl -v -H "Content-Type: application/json" -X GET {$url}
sleep 5
for i in `seq 1 10`;
do
    curl -v -H "Content-Type: application/json" -X GET {$url} &
    # sleep 1
done

