#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module to encode/decode data in the least significant bits
in PNG images
"""
from __future__ import print_function
from PIL import Image
import random
import argparse
try:
    from itertools import izip
except ImportError:
    izip = zip
    raw_input = input
from getpass import getpass

class LSBStegano(object):
    """
    Class to encode/decode data in the least significant bits
    in PNG images
    """

    #Channel to encode or decode
    C_RED, C_GREEN, C_BLUE, C_ALPHA = range(4)

    def __init__(self, image_path):
        self.image_path = image_path
        self.image = Image.open(image_path)
        self.width, self.height = self.image.size
        self.mode = self.image.mode
        self.new_im = self.image.load()

    def lin2rowcol(self, lin):
        """
        Linear to row/col address translator
        Returns a tuple with row/col address
        """
        row = int(lin / self.width)
        col = lin - int(row * self.width)
        return (col, row)

    def shuffle_k(self, key):
        """
        PRG is NOT cryptographically secure!!
        You have been warned!!
        """
        length = self.height * self.width
        lin_pos = list(range(length))

        random.seed(key)
        random.shuffle(lin_pos)
        return lin_pos

    def text_encode(self, text, key, mode=C_RED):
        """
        Encoding of text takes place here. This is the method which is directly
        Invoked from the application
        """
        #Add \x00 to know the termination pos of the string
        text += '\x00'

        #Converting string to a stream of binary
        payload = ''.join([bin(ord(x))[2:].zfill(8) for x in text])

        p_len = len(payload)

        #Checking for length requirement
        if p_len > (self.width * self.height):
            raise Exception("Error: Insufficient Size - Choose a larger image")

        pos = self.shuffle_k(key)

        for bit, l_addr in izip(payload, pos):
            #Translate linear pos to row/col address
            addr = self.lin2rowcol(l_addr)
            bit = int(bit)

            pixel = list(self.image.getpixel(addr))

            #Now modifying the LSB
            if bit:
                pixel[mode] |= 1
            else:
                pixel[mode] &= ~1

            self.new_im[addr[0], addr[1]] = tuple(pixel)
        self.image.save(''.join(self.image_path.split('.')[:-1]) + '.enc.png')

    def text_decode(self, key, mode=C_RED):
        """
        Decoding of the encoded text in self.text_encode() is done here
        Method is directly invoked from the application
        """
        pos = self.shuffle_k(key)

        #Iterate over chunks of 8
        chunk = lambda x: pos[(x * 8) : (x * 8) + 8]
        #Get the LSB value from an address
        get_val = lambda addr: str(self.image.getpixel(addr)[mode] & 1)

        i = 0
        res = ''
        while True:
            addrs = [self.lin2rowcol(x) for x in chunk(i)]
            data = ''.join([get_val(x) for x in addrs])
            char = chr(int(data, 2))
            if char != '\x00':
                res += char
            else:
                return res
            i += 1

def main():
    """
    Main function for app
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', help='enc or dec to encode or decode text respectively')
    parser.add_argument('image', help='Path to PNG image to be used')
    parser.add_argument('--message-file', help='File to read text from')
    parser.add_argument('--passphrase', help='Passphrase to use while encoding or decoding')
    args = parser.parse_args()

    if args.mode == 'enc':
        lsb = LSBStegano(args.image)
        key = args.passphrase if args.passphrase else getpass()
        print('Message:', end='')
        text = raw_input()
        lsb.text_encode(text, key)
    elif args.mode == 'dec':
        lsb = LSBStegano(args.image)
        key = args.passphrase if args.passphrase else getpass()
        print(lsb.text_decode(key))

if __name__ == '__main__':
    main()
