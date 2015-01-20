#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image
import random
from itertools import izip

class lsb_stegno:
    #Channel to encode or decode
    C_RED, C_GREEN, C_BLUE, C_ALPHA = range(4)

    def __init__(self, image_path):
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

            self.new_im[addr] = tuple(pixel)
        self.im.save("new_image.png")

def main():
    lsb = lsb_stegno("image.png")
    lsb.text_encode("someplaintext", "somekey")

    return 0

if __name__ == '__main__':
    main()
