#!/usr/bin/python3.3

import random

def roll(dice, sides):
    a = 0
    x = 1
    while x <= dice:
        a += random.randint(1, sides)
        x += 1
    return a

def best_of(dice, sides, top):
    a = []
    x = 1
    while x <= dice:
        a.append(random.randint(1, sides))
        x += 1
    a = sorted(a)
    
    y = dice - top
    p = 0
    while y < dice:
        p += a[y]
        y += 1
    return p
def statswitch(x):
    return {
        'ST': 0,
        'DX': 1,
        'CN': 2,
        'WS': 3,
        'IQ': 4,
        'CH': 5,
        'any': 7,
        }.get(x, 9)

def challenge(bonus, DC): # simplest pass/fail system in d20 format
    a = roll(1,20)
    if a == 20:
        return True
    elif (a+bonus) >= DC:
        return True
    else:
        return False

def block_roll(block):
    # Function to parse through a complicated set of rolling,
    # probably using a stack, shunting yard algoritm and reverse polish notation.  
    
    # Blocks formatted like 2d6+27 or 3d20*4d4
    
    block = list(block)
    result = list()
    operators = list()
    b = str()
    block.reverse()
    while True:
        try:
            a = block.pop()
            if isinstance(a, int):
                b += str(a)
            else:
                result.append(b)
                b = str()
                operators.append(a)
        except:
            break
        print(a)

    print(result)