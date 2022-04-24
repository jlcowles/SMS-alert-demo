"""Sender

Usage:
    sender [--delay=<ms> --stddev=<sigma> --failurerate=<rate>] 
    sender (-h | --help) 

Options:
    -h --help               Show this screen..
    --delay=<ms>            The mean delay after a sender recieves a message to simulate sending a text (in ms)  [default: 500] 
    --stddev=<sigma>         The standard deviation of the normally distributed send delay  [default: 250]
    --failurerate=<rate> The rate of messages that should fail being 'sent.'  [default: .01] 
"""
import time
import random
import json

from docopt import docopt
import redis

class Sender:
    def __init__(self):
        self.__redis = redis.Redis(host='localhost', port=6379, db=0)
        self.__message_queue = self.__redis.pubsub(ignore_subscribe_messages=True)
        self.__message_queue.subscribe('messages')

    def get_sleep_len(self, arguments):
        delay = random.normalvariate(float(arguments['--delay']), float(arguments['--stddev']))
        return abs(delay) # In case of very small mean resulting in negative delays

    def is_success(self, arguments):
        if random.random() <= float(arguments['--failurerate']):
            return False
        else:
            return True
        
    def run(self, arguments):
        # According to redis-py docs, this will block forever once the queue is empty. 
        # If we wanted to, we could avoid this by either having the producer send a kill message at the end of producing the messages, 
        # or by using get_message() and verifying if it is 'None' (indicating there is no more messages in the queue).
        # But for this usecase, blocking and waiting is fine.
        for message in self.__message_queue.listen():  
            sleep_len = self.get_sleep_len(arguments)
            isSuccess = self.is_success(arguments)
            time.sleep(sleep_len)
            self.__redis.publish('status', json.dumps({'success': isSuccess, 'delay': sleep_len}))




if __name__ == "__main__":
    arguments = docopt(__doc__)
    print(arguments)
    sender = Sender()
    sender.run(arguments)