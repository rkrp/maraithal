#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image
import random
import argparse
from itertools import izip
from sys import argv
from getpass import getpass

class lsb_stegno:
    #Channel to encode or decode
    C_RED, C_GREEN, C_BLUE, C_ALPHA = range(4)

    def __init__(self, image_path):
        self.im_path = image_path
        self.im = Image.open(image_path)
        self.width, self.height = self.im.size
        self.mode = self.im.mode
        self.new_im =  self.im.load()

    def text2binary(self, text):
        return ''.join(map(lambda x:bin(ord(x))[2:].zfill(8), text))
    
    """
    Linear to row/col address translator
    Returns a tuple with row/col address
    """
    def lin2rowcol(self, lin):
        row = lin / self.width
        col = lin - (row * self.width)
        return (col, row)
    
    """
    PRG is NOT cryptographically secure!!
    You have been warned!!
    """
    def shuffle_k(self, key):
        length = self.height * self.width
        lin_pos = range(length)

        random.seed(key)
        random.shuffle(lin_pos)
        return lin_pos
    
    """
    Encoding of text takes place here. This is the method which is directly
    invoked from the application
    """
    def text_encode(self, text, key, mode=C_RED):
        #Add \x00 to know the termination pos of the string
        text += '\x00'

        payload = self.text2binary(text)
        p_len = len(payload)

        #Checking for length requirement		
        if p_len > (self.width * self.height):
            raise Exception ("Error: Insufficient Size - Choose a larger image")

        pos = self.shuffle_k(key)

        for bit, l_addr in izip(payload, pos):
            #Translate linear pos to row/col address
            addr = self.lin2rowcol(l_addr)
            bit = int(bit)
            
            pixel = list(self.im.getpixel(addr))
 
            #Now modifying the LSB
            if bit:
                pixel[mode] |= 1
            else:
                pixel[mode] &= ~1

            self.new_im[addr[0], addr[1]] = tuple(pixel)
        self.im.save(''.join(self.im_path.split('.')[:-1]) + '.enc.png')

    """
    Decoding of the encoded text in self.text_encode() is done here
    Method is directly invoked from the application
    """
    def text_decode(self, key, mode=C_RED):
        pos = self.shuffle_k(key)
        
        #Iterate over chunks of 8
        chunk = lambda x: pos[(x * 8) : (x * 8) + 8]
        #Get the LSB value from an address
        get_val = lambda addr: str(self.im.getpixel(addr)[mode] & 1)
        
        i = 0
        res = ''
        while(True):
            addrs = map(self.lin2rowcol, chunk(i))
            data = ''.join(map(get_val, addrs))
            char = chr(int(data, 2))
            if char != '\x00':
                res += char
            else:
                return res
            i += 1

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', help='enc or dec to encode or decode text respectively')
    parser.add_argument('image', help='Path to PNG image to be used')
    parser.add_argument('--message-file', help='File to read text from')
    parser.add_argument('--passphrase', help='Passphrase to use while encoding or decoding')
    args = parser.parse_args()

    if args.mode == 'enc':
        lsb = lsb_stegno(args.image)
        key = args.passphrase if args.passphrase else getpass()
        print 'Message:',
        text = raw_input()
        lsb.text_encode(text, key)
    elif args.mode == 'dec':
        lsb = lsb_stegno(args.image)
        key = args.passphrase if args.passphrase else getpass()
        print lsb.text_decode(key)

if __name__ == '__main__':
    main()
