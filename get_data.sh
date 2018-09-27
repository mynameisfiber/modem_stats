#!/bin/bash

BASE_URL='http://192.168.100.1/cgi-bin/'
while true; do 
    echo -ne '.'
    ./modemstats.py ${BASE_URL}/status_cgi >> ./data/status.json
    ./modemstats.py ${BASE_URL}/event_cgi >> ./data/events.json
    (/usr/local/bin/speedtest --json || echo '{}') >> ./data/speedtest.json
    sleep 60s
done;
