TWDATE=`date +"%Y-%m-%d %H:%M:%S"`
TWDATE2=`date --date "10 mins ago" +"%Y-%m-%d %H:%M:%S"`
torsocks -i twint -s "covid" --until "$TWDATE" --min-wait-time 0 --since "$TWDATE2" >> tweets_cron.txt &
wait

# run every 10 min
