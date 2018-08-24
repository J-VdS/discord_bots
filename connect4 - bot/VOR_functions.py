# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 13:34:14 2018

@author: Jeroen VdS
"""

from PIL import Image
import time

W = 28; H = 25; CW = W+2; CH = H+2

images = {'R':Image.new('RGB', (W,H), color=(255,0,0)),
          'Y':Image.new('RGB', (W,H), color=(255,255,0)),
          'E':Image.new('RGB', (W,H), color=(255,255,255))
          }

def check(veld, speler):
    #horizontaal:
        for y in range(6):
            if veld[7*y:7*y+7].count(speler)>3:
                for x in range(4):
                    if veld[7*y+x:7*y+x+4] == speler*4:
                        return True
        #verticaal:
        for x in range(7):
            if veld[x::7].count(speler)>3:
                for y in range(3):
                    if veld[7*y+x:7*(y+4)+x:7] == speler*4:
                        return True
        #diagonaal linksonder naar rechtsboven
        for x in range(3,7):
            for y in range(3):
                if veld[7*y+x:7*y+x+19:6] == speler*4:
                    return True
        #diagonaal linksboven naar rechtsonder
        for x in range(4):
            for y in range(3):
                if veld[7*y+x:7*y+x+25:8] == speler*4:
                    return True

        return False

def make_img(bord):
    global W,H,CW,CH, images
    field = Image.new('RGB', (7*CW, 6*CH))
    for i in range(6):
        for j in range(7):
            field.paste(images[bord[i*7+j]], (j*CW+1, i*CH+1))
    field.save('veld.png')
    return 'veld.png'

def move(speler, veld, x):
    print(veld)
    y = veld[x::7].count('E')-1
    print(y)
    if y < 0:
        return (False,)
    veld = veld[:y*7+x]+speler+veld[y*7+x+1:]
    return (make_img(veld), veld, check(veld, speler), speler)
    




