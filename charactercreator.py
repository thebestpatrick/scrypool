#!/usr/bin/python3.3

import yaml
import cfunc
import roll
import random

import flavorgenerator as fg

#config = json.loads(open('charactersheets/examplecharacter.json').read())
# print(config["inventory"][0]["backpack"])


def merciless_stat_roll():
    arr = [roll.roll(3,6), roll.roll(3,6), roll.roll(3,6),
    roll.roll(3,6), roll.roll(3,6), roll.roll(3,6)]
    return arr


def regular_stat_roll(char_class):  ## UNFINISHED....FIXME!
    arr = [
        roll.best_of(4,6,3), roll.best_of(4,6,3), roll.best_of(4,6,3),
        roll.best_of(4,6,3), roll.best_of(4,6,3), roll.best_of(4,6,3)
    ]
    arr=sorted(arr, reverse=True)
    
    classfile = yaml.load(open('classes/' + char_class + '.yml').read())
    
    stats = ["ST", "DX", "CN", "WS", "IQ", "CH"]
    # UNFINISHED
     # basically I want this section to juggle the stats into a proper order for me,
     # based on the preferred stats of the class
    prefstats = classfile["prefstats"]
    finarr = []
    for i in stats:
        if i in prefstats:
            pass
        else:
            random.shuffle(arr)
            
    return 7


def kind_stat_roll(char_class):
    while True:
        statsok=True
        arr = [
            roll.roll(3,6), roll.roll(3,6), roll.roll(3,6),
            roll.roll(3,6), roll.roll(3,6), roll.roll(3,6)
        ]
        
        classfile = yaml.load(open('classes/' + char_class + '.yml').read())
        prefstats = classfile["prefstats"]
        
        stats = ["ST", "DX", "CN", "WS", "IQ", "CH"]
        x = 0
        for i in stats:
            if i in prefstats and arr[x] <= 14:
                statsok=False
                x += 1
            else:
                x += 1
        if statsok:
            break
    return arr


def extra_kind_stat_roll(char_class):
    while True:
        statsok=True
        arr = [
            roll.best_of(4,6,3), roll.best_of(4,6,3), roll.best_of(4,6,3),
            roll.best_of(4,6,3), roll.best_of(4,6,3), roll.best_of(4,6,3)
        ]
        
        classfile = yaml.load(open('classes/' + char_class + '.yml').read())
        prefstats = classfile["prefstats"]
        
        stats = ["ST", "DX", "CN", "WS", "IQ", "CH"]
        x = 0
        for i in stats:
            if i in prefstats and arr[x] <= 14:
                statsok = False
                x += 1
            else:
                x += 1
        if statsok:
            break
    return arr


def lists_overlap(a, b):
    for i in a:
        if i in b:
            return True
    return False


## Good format for other prereq checkers
def check_stat_prereqs(prereq, charactersheet):  # True = passed prereq challenge
    try:
        a = prereq.split()
        if int(charactersheet[a[0]]) >= int(a[1]):
            return True
        else: 
            return False
        
    except:
    # not fond of failing this on an exception...
    # maybe null instead?
        return False


def pick_feat(tags, character_file):  # tags is a list
## Totally threw out everything here. starting fresh
## git commit 68c8cdfbbc66322545ac910e29b6f8205113b60a had last version

    characterfile = yaml.load(str(character_file))
    feats = yaml.load(open("feats.yml"))
    random.shuffle(feats)
    ranktobeat = 0
    for f in feats:    
        # make sure its not already picked
        try:
            if f["name"] in characterfile["feats"]:
                continue
        except:
            pass
            
        ## check prereqs
        
        # # # # WORK GOES HERE # # # #
        passing = [True, ] # any falses in the list fails everything
        try: 
            for s in f["prereqs"]["stats"]:
                passing.append(check_stat_prereqs(str(s), characterfile))
        except: pass
        if False in passing:
            continue
        ## end of prereq checking
        
        ## rank f
        rank = f["score"]
        
        for x in tags:
            if x in f["tags"]: rank += 10 # add ten for every matching tag.

        # add twenty if the class is called out.
        if characterfile["class"] in f["tags"]: rank += 20

        # if the name of the feat is tagged, probably want to give it to them
        if f["name"] in tags: rank += 75
        
        ## end of rankings, make call
        if rank > ranktobeat:
            finalchoice = f["name"]
        elif rank < ranktobeat:
            pass
        else:
            # flip coin
            if roll.roll(1,6) >= 1: finalchoice = f["name"]
        print(str(f["name"]) + " : " + str(rank))
    return finalchoice


def parse_specials(character_file):
    # A function for taking race and class special features, like bonus feat,
    # and turning them into the thing that they mean, then returning the proper 
    # list of specials.
    finlist = list()
    characterfile = yaml.load(character_file)
    
    for s in characterfile["specials"]:
        if isinstance(s, list):
            alpha = random.choice(s)
            characterfile["specials"].remove(s)
            characterfile["specials"].append(alpha)
            parse_specials(yaml.dump(characterfile))
        elif s == "bonus feat":
            # pick a generic bonus feat
            print("picking bonus feat")
            characterfile["specials"].remove(s)
            characterfile["feats"].append(pick_feat(["mobility", ], characterfile)) # FIXME since mobility isn't the only tag
        elif s == "fighter bonus feat":
            # pick a fighter bonus feat
            print("picking fighter bonus feat")
            characterfile["specials"].remove(s)
        else: 
            # stuff
            pass  # doing nothing I guess?
    return characterfile


def yaml_create_character(char_race, char_class, mods): # Seems rather slow and clunking, will need optimizing
    # take care of this top line elsewhere
    # finale = "!!python/object:__main__.entity\n"
    genders = ["m", "f"]
    gender = random.choice(genders)
    name = fg.gen_name(gender, char_race)
    finale = "name: " + name + "\n"
    finale += "gender: " + gender + "\n"
    finale += "race: " + char_race + "\n"
    finale += "symbol: " + fg.coatofarms_gen() + "\n"
    finale += "class: " + char_class + "\n"

    initstats = kind_stat_roll(char_class)
    
    ## Open the needed files and make sure they work before we go farther
    ## Should probably, at some point, move these to a database access system.
    try:
        racefile = yaml.load(open('races/' + char_race + '.yml').read())
    except:
        print("could not open race file yaml")
    try:
        classfile = yaml.load(open('classes/' + char_class + '.yml').read())
    except:
        print("could not open class file yaml")

    ## Apply Racial Bonuses
    adstats = cfunc.apply_race_stats(initstats, racefile, classfile)
    #print(adstats)
    ## Make sure all of the stat values are possible.
    a = 0
    stats = ["ST", "DX", "CN", "WS", "IQ", "CH"]
    for i in adstats:
        if i < 3:
            adstats[a] = 3
        else:
            pass
        finale += stats[a] + ": " + str(adstats[a]) + "\n"
        a += 1
    
    finale += "size: " + racefile["size"] + "\n"
    finale += "speed: " + str(racefile["speed"]) + "\n"
    finale += "feats: \n- " + pick_feat(["mobility", "melee"], finale) + "\n" # FIXME: don't always pass mobility
    
    ##
    ## this section could be chopped out and moved to the 'level up' function, since its just
    ## adding a level one of a class to an existing character. Or it could handle it here 
    ## since it is kind of unique handling at level one.  
    ## 
    
    finale += "total hp: " + str(classfile["hit die"] + cfunc.nstatmod(adstats[2])) + "\n"
    finale += "current hp: " + str(classfile["hit die"] + cfunc.nstatmod(adstats[2])) + "\n"
    finale += "base attack: " + str(classfile["level 1"]["baseattack"]) + "\n"
    finale += "fort save: " + str(classfile["level 1"]["fortsave"]) + "\n"
    finale += "reflex save: " + str(classfile["level 1"]["refsave"]) + "\n"
    finale += "will save: " + str(classfile["level 1"]["willsave"]) + "\n"
    
    ##
    ## this section here definitely deserves special treatment
    ## like to add specific skills when called for, or add bonus feats
    ## when necessary, without cluttering the specials section of 
    ## the character sheet
    ## 
    
    # check both race file and class file for their respective specials
    speclist = classfile["level 1"]["special"] + racefile["race specials"]
    finale += "specials: \n" +  yaml.dump(speclist, default_flow_style=False) + "\n"
    
    # Pass the string in for post processing, things like feat assignment and some 
    # parsing work regarding it.
    
    finale = parse_specials(finale)

    return finale
