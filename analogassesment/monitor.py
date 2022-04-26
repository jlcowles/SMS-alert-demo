"""Monitor

Usage:
    monitor [--refreshtime=<s>] 
    monitor (-h | --help) 

Options:
    -h --help            Show this screen..
    --refreshtime=<s>    The number of seconds between refreshing the monitor  [default: 30]  
"""
import time
import json

from docopt import docopt
import redis


class Monitor:
    PRINT_FORMAT = 'Total messages: {} Failed messages: {} Avg delay: {}'
    def __init__(self):
        self.__redis = redis.Redis(host='localhost', port=6379, db=0)
        self.__total_messages = 0
        self.__failed_messages = 0
        self.__average = 0

    def update_data(self, data):
        self.__total_messages += 1
        if not data['success']:
            self.__failed_messages += 1
        # See https://math.stackexchange.com/a/1567345
        self.__average = self.__average + ((data['delay'] - self.__average) / self.__total_messages)
    
    def read_and_update_status(self):
        while self.__redis.llen('status') > 0:
            message = self.__redis.lpop('status').decode()
            message_data = json.loads(message)
            self.update_data(message_data)

    def run(self, arguments):
        print('Starting monitor.')
        # Yes it will loop forever, but that's fine for a monitoring app that is expected to run for basically forever
        while True:
            self.read_and_update_status()

            print(self.PRINT_FORMAT.format(self.__total_messages, self.__failed_messages, self.__average))
            time.sleep(float(arguments['--refreshtime']))






if __name__ == "__main__":
    arguments = docopt(__doc__)
    monitor = Monitor()
    monitor.run(arguments)