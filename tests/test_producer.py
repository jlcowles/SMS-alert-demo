from unittest.mock import MagicMock
from smsdemo.producer import Producer

def test_gen_phone_number():
    ret = list(Producer().generate_n_phonenumbers(10))
    assert 10 == len(ret)
    for num in ret:
        assert 9 == len(num)

def test_gen_message():
    ret = list(Producer().generate_n_msg(10))
    assert 10 == len(ret)
    for msg in ret:
        assert 1 <= len(msg) <= 100
        
def test_publish_called():
    prd = Producer()
    mock_method = MagicMock(return_value=0)
    prd.publish = mock_method
    prd.run({'--num': 5})
    assert 5 == mock_method.call_count

