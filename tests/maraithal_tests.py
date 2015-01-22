from nose.tools import *
from maraithal.lsbstegano import LSBStegano
from os.path import isfile

filename = 'tests/test.png'
key = 'some key'
text = 'Some sample text which will be encoded'
newfile = ''.join(filename.split('.')[:-1]) + '.enc.png'

def setup():
    pass

def teardown():
    pass

def test_encode():
    lsb = LSBStegano(filename)
    lsb.text_encode(text, key)
    assert isfile(newfile)

def test_decode():
    lsb = LSBStegano(newfile)
    assert lsb.text_decode(key) == text

