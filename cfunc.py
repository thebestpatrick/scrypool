#!/usr/bin/python3.3
## A holding file for misc. character related files.

import roll
import random
import math


def has_feat(character, feat):
    """Given character and feat, checks to see if character has feat."""
    try:
        return character["feats"][feat]
    except:
        return False


def get_skill_points(character, skill):
    """Returns number of skill points in a skill"""
    try:
        return character["skills"][skill]
    except:
        return 0


def check_class_level(character, charclass):
    """Checks number of levels in a specific class for a character"""
    try:
        return character["levels"][charclass]
    except:
        return 0


def get_total_level(character):
    """Returns total character level"""
    arr = character["levels"]
    tlev = 0
    for i in arr:
        tlev += check_class_level(character, i)
    return tlev


def get_caster_level(char_file):
    """Returns total caster level"""
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

# wants the racefile and classfile pre-opened and nice
def apply_race_stats(initstats, racefile, classfile):
    """Applies racial stat bonuses"""
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


def statmod(stat):
    """Returns the stat modifier of a stat"""
    return math.floor((stat-10) / 2)


def nstatmod(stat):
    """Like statmod() but less than zero is zero"""
    a = math.floor( (stat-10) / 2)
    if a <= 0:
        return 0
    else:
        return a


# wants the racefile and classfile pre-opened and nice
def remove_race_stats(initstats, racefile, classfile):
    """Removes the racial stat bonuses."""
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