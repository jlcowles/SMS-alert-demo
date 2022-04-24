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
    def __init__(self):
        r = redis.Redis(host='localhost', port=6379, db=0)
        self.__status_queue = r.pubsub(ignore_subscribe_messages=True)
        self.__status_queue.subscribe('status')
        self.__total_messages = 0
        self.__failed_messages = 0
        self.__average = 0

    def update_data(self, data):
        self.__total_messages += 1
        if not data['success']:
            self.__failed_messages += 1
        # See https://math.stackexchange.com/a/1567345
        self.__average = self.__average + ((data['delay'] - self.__average) / self.__total_messages)

    def run(self, arguments):
        while True:
            message = self.__status_queue.get_message()
            if message: # If message is None then we have gotten everything in the queue and should be wait again
                message_data = json.loads(message['data'].decode())
                self.update_data(message_data)
            else:
                print('Total messages: ' + str(self.__total_messages) + ' Failed messages: ' + str(self.__failed_messages) + ' Avg delay: ' + str(self.__average)) #TODO str format instead of this
                time.sleep(float(arguments['--refreshtime']))






if __name__ == "__main__":
    arguments = docopt(__doc__)
    print(arguments)
    monitor = Monitor()
    monitor.run(arguments)