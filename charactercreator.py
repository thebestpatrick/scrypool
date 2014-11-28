#!/usr/bin/python3.3

import yaml
import cfunc
import roll
import random

import flavorgenerator as fg

#config = json.loads(open('charactersheets/examplecharacter.json').read())
# print(config["inventory"][0]["backpack"])


def merciless_stat_roll():
    """Rolls 3d6 and sticks you with the result.  Probably not the best idea for most purposes."""
    arr = [
        roll.roll(3, 6), roll.roll(3, 6), roll.roll(3, 6),
        roll.roll(3, 6), roll.roll(3, 6), roll.roll(3, 6)
    ]
    return arr


def regular_stat_roll(char_class):  # UNFINISHED....FIXME!
    """Rolls 4d6, picks the best 3.  Then puts the best results on the appropriate ability scores"""
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
    """Rolls 3d6, then makes sure that all important stats are above 13"""
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
    """Rolls 4d6, picks best three, then makes sure all the important stats are over 13"""
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
    """Checks to see if there is any overlap between two lists"""
    for i in a:
        if i in b:
            return True
    return False


## Good format for other prereq checkers
def check_stat_prereqs(prereq, charactersheet):
    """Returns True if the prereqs are met, false if they aren't.  Returns False also on exception"""
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
    """Picks a feat using score rankings on the list."""
    # Not super efficient, so don't call it too much
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
    """A function for taking race and class special features, like bonus feat,
    and turning them into the thing that they mean, then returning the proper list of specials."""
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


def pick_init_skills(character_file, class_skills):
    """Only useful during character creation, really this should all get the same treatment of feats...
    but that sounds hard, and no one cares about skills anyway."""
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
    """Given a race and class, returns a yaml formatted character sheet"""
    genders = ["m", "f"]
    gender = random.choice(genders)
    name = fg.gen_name(gender, char_race)
    char_sheet = "name: " + name + "\n"
    char_sheet += "gender: " + gender + "\n"
    char_sheet += "race: " + char_race + "\n"
    # char_sheet += "symbol: " + fg.coatofarms_gen() + "\n"
    char_sheet += "class: \n  " + char_class + ": 1\n"

    initstats = kind_stat_roll(char_class)
    
    ## Open the needed files and make sure they work before we go farther
    ## Should probably, at some point, move these to a database access system.

    racefile = yaml.load(open('races/' + char_race + '.yml').read())

    classfile = yaml.load(open('classes/' + char_class + '.yml').read())

    char_sheet += "base attack: " + str(classfile["level 1"]["baseattack"]) + "\n"

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
        char_sheet += stats[a] + ": " + str(adstats[a]) + "\n"
        a += 1

    # check both race file and class file for their respective specials
    speclist = classfile["level 1"]["special"] + racefile["race specials"]
    char_sheet += "specials: \n" + yaml.dump(speclist, default_flow_style=False) + "\n"

    char_sheet += "size: " + racefile["size"] + "\n"
    char_sheet += "speed: " + str(racefile["speed"]) + "\n"
    char_sheet += "skills: \n  " + pick_init_skills(char_sheet, classfile["class skills"]) + "\n"
    char_sheet += "feats: \n- " + pick_feat(mods, char_sheet) + "\n"
    
    ##
    ## this section could be chopped out and moved to the 'level up' function, since its just
    ## adding a level one of a class to an existing character. Or it could handle it here 
    ## since it is kind of unique handling at level one.  
    ## 
    
    char_sheet += "total hp: " + str(classfile["hit die"] + cfunc.nstatmod(adstats[2])) + "\n"
    char_sheet += "current hp: " + str(classfile["hit die"] + cfunc.nstatmod(adstats[2])) + "\n"
    char_sheet += "fort save: " + str(classfile["level 1"]["fortsave"]) + "\n"
    char_sheet += "reflex save: " + str(classfile["level 1"]["refsave"]) + "\n"
    char_sheet += "will save: " + str(classfile["level 1"]["willsave"]) + "\n"
    alignment = fg.pick_alignment(list(classfile["alignment"]))
    char_sheet += "alignment: " + alignment + "\n"
    char_sheet += "deity: " + str(fg.pick_deity(alignment)) + "\n"

    if str(classfile["magic type"]) == "None":
        pass
    elif str(classfile["magic type"]) == "Arcane":
        pass
        # Handle Wizard and sorcerer spell formation here
    elif str(classfile["magic type"]) == "Bard":
        pass
        # Handle bard spell formation here
    elif str(classfile["magic type"]) == "Divine":
        pass
        # Handle cleric and similar spell formation
    elif str(classfile["magic type"]) == "Druid":
        pass
        # Handle druid spell formation
    elif str(classfile["magic type"]) == "Paladin":
        pass
        # Handle Paladin spell formation
    elif str(classfile["magic type"]) == "Ranger":
        pass
        # Handle Ranger spell formation\
    else:
        pass
        # Might be tricky, but handle this oddity some other way
    
    ##
    ## this section here definitely deserves special treatment
    ## like to add specific skills when called for, or add bonus feats
    ## when necessary, without cluttering the specials section of 
    ## the character sheet
    ## 

    # Pass the string in for post processing, things like feat assignment and some 
    # parsing work regarding it.
    
    char_sheet = parse_specials(char_sheet)

    return char_sheet
