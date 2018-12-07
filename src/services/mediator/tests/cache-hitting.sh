curl -v -H "Content-Type: application/json" -X GET http://localhost:9027/audioclips/search?pattern=dog
sleep 5
for i in `seq 1 10`;
do
    curl -v -H "Content-Type: application/json" -X GET http://localhost:9027/audioclips/search?pattern=dog &
    # sleep 1
done

