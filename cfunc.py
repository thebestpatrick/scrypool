#!/usr/bin/python3.3
## A holding file for misc. character related files.

import roll
import random
import math


## Make sure a character has a feat.
def has_feat(character, feat):
    try:
        return character["feats"][feat]
    except:
        return False


## See how many skill points a character has in a skill
def get_skill_points(character, skill):
    try:
        return character["skills"][skill]
    except:
        return 0


## Check how many levels of a particular class a character has
def check_class_level(character, charclass):
    try:
        return character["levels"][charclass]
    except:
        return 0


## Get the total level of a character
def get_total_level(character):
    arr = character["levels"]
    tlev = 0
    for i in arr:
        tlev += check_class_level(character, i)
    return tlev


def get_caster_level(char_file):
    # https://docs.python.org/3.3/library/stdtypes.html#dict
    # maybe use get here?
    cl = 0
    # WIZARD
    try:
        cl += char_file["class"]["wizard"]
    except:
        cl += 0
    # SORCERER
    try:
        cl += char_file["class"]["sorcerer"]
    except:
        cl += 0
    # BARD
    try:
        cl += char_file["class"]["bard"]
    except:
        cl += 0
    # CLERIC
    try:
        cl += char_file["class"]["cleric"]
    except:
        cl += 0
    return cl


## Apply race stat bonuses
def apply_race_stats(initstats, racefile, classfile): # wants the racefile and classfile pre-opened and nice
    arr = racefile["statmods"]
    for i in arr:
        a = roll.statswitch(i)
        if a == 7:
            try:
                c = random.choice(classfile["prefstats"])
                a = roll.statswitch(c)
            except:
                print("prefstats error in apply_race_stats")
        try:
            initstats[a] += racefile["statmods"][i]
        except:
            print("apply_race_stats error " + i)
    return initstats


## Get stat mod
def statmod(stat):
    return math.floor( (stat-10) / 2)


## Gets stat mod but ignores negatives
def nstatmod(stat):
    a = math.floor( (stat-10) / 2)
    if a <= 0:
        return 0
    else:
        return a


## Remove race stat bonuses
def remove_race_stats(initstats, racefile, classfile): # wants the racefile and classfile pre-opened and nice
    arr = racefile["statmods"]
    for i in arr:
        a = roll.statswitch(i)
        if a == 7:
            try:
                c = random.choice(classfile["prefstats"])
                a = roll.statswitch(c)
            except:
                print("prefstats error in apply_race_stats")
        try:
            initstats[a] += -1 * racefile["statmods"][i]
        except:
            print("remove_race_stats error " + i)
    return initstats


## Add a level of a class 
def add_level(character, char_class):
    return 0