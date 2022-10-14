for i in {1..1000000}
do
    TWDATE=`tail -n 100 tweets.txt | grep ^[0-9] | tail -n 1 | cut -d" " -f2,3`
    TWDATE2=`date --date "$TWDATE 1 day ago" +"%Y-%m-%d %H:%M:%S"`
    torsocks -i twint -s "covid" --until "$TWDATE" --min-wait-time 0 --since "$TWDATE2" >> tweets.txt &
    wait
done

# hourly execute `pkill twint` 
# hourly execute `rm core.*`
