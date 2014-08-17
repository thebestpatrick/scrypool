#!/usr/bin/python3.3

import yaml
import cfunc
import roll
import random

import flavorgenerator as fg

#config = json.loads(open('charactersheets/examplecharacter.json').read())
# print(config["inventory"][0]["backpack"])


def merciless_stat_roll():
    arr = [
        roll.roll(3, 6), roll.roll(3, 6), roll.roll(3, 6),
        roll.roll(3, 6), roll.roll(3, 6), roll.roll(3, 6)
    ]
    return arr


def regular_stat_roll(char_class):  # UNFINISHED....FIXME!
    arr = [
        roll.best_of(4, 6, 3), roll.best_of(4, 6, 3), roll.best_of(4, 6, 3),
        roll.best_of(4, 6, 3), roll.best_of(4, 6, 3), roll.best_of(4, 6, 3)
    ]
    arr = sorted(arr, reverse=True)
    
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
    classfile = yaml.load(open('classes/' + char_class + '.yml').read())
    prefstats = classfile["prefstats"]

    while True:
        statsok = True
        arr = [
            roll.roll(3, 6), roll.roll(3, 6), roll.roll(3, 6),
            roll.roll(3, 6), roll.roll(3, 6), roll.roll(3, 6)
        ]
        
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


def extra_kind_stat_roll(char_class):
    classfile = yaml.load(open('classes/' + char_class + '.yml').read())
    prefstats = classfile["prefstats"]
    while True:
        arr = [
            roll.best_of(4, 6, 3), roll.best_of(4, 6, 3), roll.best_of(4, 6, 3),
            roll.best_of(4, 6, 3), roll.best_of(4, 6, 3), roll.best_of(4, 6, 3)
        ]
        
        stats = ["ST", "DX", "CN", "WS", "IQ", "CH"]
        x = 0
        for i in stats:
            if i in prefstats and arr[x] <= 14:
                continue
            else:
                x += 1
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
    finalchoice = "Toughness"  # just so it has a default.

    # Load the feats there are now for later use
    try:
        charfeats = characterfile["feats"]
    except:
        charfeats = []
    for f in feats:
        ## rank f
        rank = f["score"]
        # make sure its not already picked
        try:
            if f["name"] in characterfile["feats"]:
                continue
        except:
            pass

        # if its a fighter bonus, then it must hold
        if "fighter bonus" in tags and "fighter bonus" not in f["tags"]:
            continue

        ## check prereqs
        
        # # # # WORK GOES HERE # # # #

        try:
            if f["prereqs"]["caster level"] > cfunc.get_caster_level(characterfile):
                continue
        except:
            pass
        passing = [True, ]  # any falses in the list fails everything

        # Check stat prereqs
        try: 
            for s in f["prereqs"]["stats"]:
                z = check_stat_prereqs(str(s), characterfile)
                if z:
                    rank += 5
                else:
                    pass
                passing.append(z)
        except:
            pass
        if False in passing:
            continue

        # Check Base attack prereq
        try:
            if f["prereqs"]["base attack"] >= characterfile["base attack"]:
                stupidcrap = f + " wut?"  # FIXME I have no idea what this does...
                # if you remove stupid crap here...the whole thing breaks when
                # a feat has a base attack requirement?  what the actual fuck?
                continue
            else:
                rank += 5
        except:
            pass  # but make sure base attack is set before calling this!

        # Check Feats prereqs
        preqs = []
        try:
            preqs = f["prereqs"]["feats"]
        except:
            pass  # there are no feat prereqs, keep rolling

        passing = [True, ]  # any falses in the list fails everything
        for x in preqs:
            if x in charfeats:
                rank += 20
            else:
                passing.append(False)
        if False in passing:
            continue
        ## end of prereq checking

        for x in tags:
            if x in f["tags"]:
                rank += 10  # add ten for every matching tag.

        # add twenty if the class is called out.
        if characterfile["class"] in f["tags"]:
            rank += 20

        # if the name of the feat is tagged, probably want to give it to them
        if f["name"] in tags:
            rank += 175
        
        ## end of rankings, make call
        if rank > ranktobeat:
            finalchoice = f["name"]
            ranktobeat = rank
        elif rank < ranktobeat:
            pass
        else:
            # pick randomly
            if roll.roll(1, 3) >= 1:
                finalchoice = f["name"]
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
            characterfile["specials"].remove(s)
            characterfile["feats"].append(pick_feat([], characterfile))  # FIXME maybe get tags arg 1?
        elif s == "fighter bonus feat":
            # pick a fighter bonus feat
            characterfile["specials"].remove(s)
            characterfile["feats"].append(pick_feat(["fighter bonus", ], characterfile))
        else: 
            # stuff
            pass  # doing nothing I guess?
    return characterfile


def pick_skills(character_file, class_skills):  # Only useful during character creation.
    # really this should all get the same treatment of feats...
    # but that sounds hard, and no one cares about skills anyway.
    characterfile = yaml.load(str(character_file))

    for key in characterfile["class"]:  # like this won't work except in creation.
        classfile = yaml.load(open('classes/' + key + '.yml').read())

    # Get skill points
    skill_points = cfunc.statmod(characterfile["IQ"]) + classfile["skills per rank"]
    if "skilled" in characterfile["specials"]:
        skill_points += 1
    x = 0
    skills = ""
    random.shuffle(class_skills)
    if skill_points <= 0:
        skill_points = 1
    while x < skill_points:
        # Get new class skills
        skills += class_skills.pop() + ": 1 \n  "
        # FIXME might get an error here with more skill points than skills
        # Pick random skills?  should never happen
        x += 1
    return skills


def yaml_create_character(char_race, char_class, mods):  # Seems rather slow and clunking, will need optimizing
    genders = ["m", "f"]
    gender = random.choice(genders)
    name = fg.gen_name(gender, char_race)
    finale = "name: " + name + "\n"
    finale += "gender: " + gender + "\n"
    finale += "race: " + char_race + "\n"
    # finale += "symbol: " + fg.coatofarms_gen() + "\n"
    finale += "class: \n  " + char_class + ": 1\n"

    initstats = kind_stat_roll(char_class)
    
    ## Open the needed files and make sure they work before we go farther
    ## Should probably, at some point, move these to a database access system.

    racefile = yaml.load(open('races/' + char_race + '.yml').read())

    classfile = yaml.load(open('classes/' + char_class + '.yml').read())

    finale += "base attack: " + str(classfile["level 1"]["baseattack"]) + "\n"

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

    # check both race file and class file for their respective specials
    speclist = classfile["level 1"]["special"] + racefile["race specials"]
    finale += "specials: \n" + yaml.dump(speclist, default_flow_style=False) + "\n"

    finale += "size: " + racefile["size"] + "\n"
    finale += "speed: " + str(racefile["speed"]) + "\n"
    finale += "skills: \n  " + pick_skills(finale, classfile["class skills"]) + "\n"
    finale += "feats: \n- " + pick_feat(mods, finale) + "\n"
    
    ##
    ## this section could be chopped out and moved to the 'level up' function, since its just
    ## adding a level one of a class to an existing character. Or it could handle it here 
    ## since it is kind of unique handling at level one.  
    ## 
    
    finale += "total hp: " + str(classfile["hit die"] + cfunc.nstatmod(adstats[2])) + "\n"
    finale += "current hp: " + str(classfile["hit die"] + cfunc.nstatmod(adstats[2])) + "\n"
    finale += "fort save: " + str(classfile["level 1"]["fortsave"]) + "\n"
    finale += "reflex save: " + str(classfile["level 1"]["refsave"]) + "\n"
    finale += "will save: " + str(classfile["level 1"]["willsave"]) + "\n"
    
    ##
    ## this section here definitely deserves special treatment
    ## like to add specific skills when called for, or add bonus feats
    ## when necessary, without cluttering the specials section of 
    ## the character sheet
    ## 

    # Pass the string in for post processing, things like feat assignment and some 
    # parsing work regarding it.
    
    finale = parse_specials(finale)

    return finale
