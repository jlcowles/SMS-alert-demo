#!/usr/bin/bash

# Run tests
python3 -m pytest

# Clear out the redis lists in case of pollution
redis-cli flushall


python3 smsdemo/producer.py &
#If we don't wait for a second than occasionally one of the senders will start first, see the list is empty, and quit immediately
sleep .5


python3 smsdemo/sender.py &
python3 smsdemo/sender.py &
python3 smsdemo/sender.py &


python3 smsdemo/monitor.py --refreshtime=5