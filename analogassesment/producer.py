"""Producer

Usage:
    producer [--num=<count>] 
    producer (-h | --help) 

Options:
    -h --help     Show this screen..
    --num=<count> The number of messages to generate  [default: 1000] 
"""
import random
import string

from docopt import docopt
import redis

class Producer:
    #According to what I can tell from quick search, SMS messages actually use an extension of the Latin-9 charset called 'GSM 03.38' 
    # But given we are already limiting ourselves to only US numbers (see docs for 'generate_n_phonenumbers') 
    # we will just use the ascii charset for now for convenience sake, although obviously this could be extended fairly easily
    __charset = string.ascii_letters + string.digits + string.punctuation 
    def __init__(self):
        self.__redis = redis.Redis(host='localhost', port=6379, db=0)

    def publish(self, elmt):
        self.__redis.publish('messages', elmt)

    def generate_n_msg(self, n):
        count = 0
        strLen = random.randint(1, 100)
        while count < n:
            yield ''.join(random.choices(self.__charset, k=strLen))
            count += 1

    # In theory, we could use the python-phonenumbers module here, but that only validates numbers, not generate them. 
    # Similarly, we could extend this method to generate e.164 numbers (or even local numbers), 
    # but I am considering that out of scope, as properly generating phone numbers globally is a non trivial problem of it's own.
    def generate_n_phonenumbers(self, n):
        count = 0
        while count < n:
            yield ''.join([str(random.randint(0,9)) for x in range(9)])
            count += 1

    def run(self, arguments):
        elmt_count = arguments['--num']
        for elmt in zip(self.generate_n_phonenumbers(int(elmt_count)), self.generate_n_msg(int(elmt_count))):
            self.publish(str(elmt))


if __name__ == "__main__":
    arguments = docopt(__doc__)
    prd = Producer()
    prd.run(arguments)