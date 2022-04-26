#!/usr/bin/bash

# Run tests
python3 -m pytest

# Clear out the redis lists in case of pollution
redis-cli flushall


python3 analogassesment/producer.py &
#If we don't wait for a second than occasionally one of the senders will start first, see the list is empty, and quit immediately
sleep .5


python3 analogassesment/sender.py &
python3 analogassesment/sender.py &
python3 analogassesment/sender.py &


python3 analogassesment/monitor.py --refreshtime=5