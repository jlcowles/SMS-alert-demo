from unittest.mock import patch
from smsdemo.sender import Sender

# TODO this isn't really a good test, and is mostly just testing stdlib methods
def test_get_sleep_len():
    sender = Sender()
    with patch('random.normalvariate', return_value=1.0):
        assert 1.0 == sender.get_sleep_len({'--delay':0, '--stddev':0})

def test_get_sleep_len():
    sender = Sender()
    with patch('random.random', return_value=.5):
        assert not sender.is_success({'--failurerate': .7})
        assert sender.is_success({'--failurerate': .4})