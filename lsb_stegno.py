#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image

class lsb_stegno:
    def __init__(self, image_path):
        self.im = Image.open(image_path)
        self.width, self.height = self.im.size
        self.mode = self.im.mode
        self.new_im =  self.im.load()

    def text2binary(self, text):
        return ''.join(map(lambda x:bin(ord(x))[2:].zfill(8), text))

    def text_encode(self, text):
        payload = self.text2binary(text)
        payload_length = len(payload)

        #Checking for length requirement		
        if payload_length > (self.width * self.height):
            raise Exception ("Error: Insufficient Size - Choose a larger image")

        #Iterating through the rows
        rp = 0	#Row Pointer
        cp = 0	#Col Pointer
        i = 0

        for i in payload:
            original = self.im.getpixel((cp,rp))
            #Now modifying the LSB
            mod = bin(original[0])[:-1] + i
            self.new_im[cp, rp] = (int(mod, 2), original[1], original[2], original[3])

            #Moving the row and col pointers
            if(cp == self.width - 1):
                cp = 0
                rp += 1
            else:
                cp += 1
    
        self.im.save("new_image.png")

def main():
    lsb = lsb_stegno("image.png")
    lsb.text_encode("SomeText")

    return 0

if __name__ == '__main__':
    main()
