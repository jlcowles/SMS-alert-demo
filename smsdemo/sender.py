"""Sender - Note this must be ran AFTER a producer

Usage:
    sender [--delay=<ms> --stddev=<sigma> --failurerate=<rate>] 
    sender (-h | --help) 

Options:
    -h --help               Show this screen..
    --delay=<ms>            The mean delay after a sender recieves a message to simulate sending a text (in ms)  [default: 500] 
    --stddev=<sigma>        The standard deviation of the normally distributed send delay  [default: 250]
    --failurerate=<rate>    The rate of messages that should fail being 'sent.'  [default: .05] 
"""
import time
import random
import json

from docopt import docopt
import redis

class Sender:
    def __init__(self):
        self.__redis = redis.Redis(host='localhost', port=6379, db=0)

    def get_sleep_len(self, arguments):
        delay = random.normalvariate(float(arguments['--delay']), float(arguments['--stddev']))
        return abs(delay) # In case of very small mean resulting in negative delays

    def is_success(self, arguments):
        if random.random() <= float(arguments['--failurerate']):
            return False
        else:
            return True
        
    def run(self, arguments):
        while self.__redis.llen('messages') > 0:
            self.__redis.lpop('messages') # We currently don't actually do anything with the message
            sleep_len = self.get_sleep_len(arguments)
            isSuccess = self.is_success(arguments)
            # Divide by 1000 to change to ms
            time.sleep(sleep_len/1000)
            self.__redis.lpush('status', json.dumps({'success': isSuccess, 'delay': sleep_len}))
        print('SENDER: Messages queue is empty, exiting...')




if __name__ == "__main__":
    arguments = docopt(__doc__)
    sender = Sender()
    sender.run(arguments)