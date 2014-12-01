#!/usr/bin/python3.3

import yaml
import math
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
    
    classfile = yaml.safe_load(open('classes/' + char_class + '.yml').read())
    
    stats = ["ST", "DX", "CN", "WS", "IQ", "CH"]
    # UNFINISHED
     # basically I want this section to juggle the stats into a proper order for me,
     # based on the preferred stats of the class
    prefstats = classfile["prefstats"]
    for i in stats:
        if i in prefstats:
            pass
        else:
            random.shuffle(arr)
            
    return 7


def kind_stat_roll(char_class):
    """Rolls 3d6, then makes sure that all important stats are above 13"""
    classfile = yaml.safe_load(open('classes/' + char_class + '.yml').read())
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
    classfile = yaml.safe_load(open('classes/' + char_class + '.yml').read())
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
    """Picks a feat using score rankings on the list.  Returns feat as single entry list"""
    # Not super efficient, so don't call it too much
## Totally threw out everything here. starting fresh
## git commit 68c8cdfbbc66322545ac910e29b6f8205113b60a had last version

    # characterfile = yaml.safe_load(str(character_file))
    feats = yaml.safe_load(open("feats.yml"))
    random.shuffle(feats)
    ranktobeat = 0
    finalchoice = "Toughness"  # just so it has a default.

    # Load the feats there are now for later use
    try:
        charfeats = character_file["feats"]
    except:
        charfeats = []
    for f in feats:
        ## rank f
        rank = f["score"]
        # make sure its not already picked
        try:
            if f["name"] in character_file["feats"]:
                continue
        except:
            pass

        # if its a fighter bonus, then it must hold
        if "fighter bonus" in tags and "fighter bonus" not in f["tags"]:
            continue

        ## check prereqs
        
        # # # # WORK GOES HERE # # # #

        try:
            if f["prereqs"]["caster level"] > cfunc.get_caster_level(character_file):
                continue
        except:
            pass
        passing = [True, ]  # any falses in the list fails everything

        # Check stat prereqs
        try: 
            for s in f["prereqs"]["stats"]:
                z = check_stat_prereqs(str(s), character_file)
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
            if f["prereqs"]["base attack"] >= character_file["base attack"]:
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
        if character_file["class"] in f["tags"]:
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
    return [finalchoice, ]


def parse_specials(character_file):
    """A function for taking race and class special features, like bonus feat and domains,
    and turning them into the thing that they mean, then returning the proper list of specials."""
    finlist = list()
    # characterfile = yaml.safe_load(character_file)
    
    for s in character_file["specials"]:
        if isinstance(s, list):
            alpha = random.choice(s)
            character_file["specials"].remove(s)
            character_file["specials"].append(alpha)
            parse_specials(yaml.dump(character_file))
        elif s == "bonus feat":
            # pick a generic bonus feat
            character_file["specials"].remove(s)
            character_file["feats"] += pick_feat([], character_file)  # FIXME maybe get tags arg 1?
        elif s == "fighter bonus feat":
            # pick a fighter bonus feat
            character_file["specials"].remove(s)
            character_file["feats"] += pick_feat(["fighter bonus", ], character_file)
        elif s == "domains":
            deities = yaml.safe_load(open('deities.yml').read())
            domains = ["failure", "unusual errors"]
            for zzz in deities:
                if zzz["name"] == character_file["deity"]:
                    domains = pick_domains(zzz["domains"])
                    break
                else:
                    pass
            #characterfile += "domains: \n- " + domains[0] + "\n- " + domains[1] + "\n"
            character_file["domains"] = domains
        else: 
            # stuff
            pass  # doing nothing I guess?
    return character_file


def pick_init_skills(character_file, class_skills):
    """
    Picks out a suite of skills from class skills and adds them to character file in form skill: 1
    Only useful during character creation, really this should all get the same treatment of feats...
    but that sounds hard, and no one cares about skills anyway.
    """
    # characterfile = yaml.safe_load(str(character_file))

    for key in character_file["class"]:  # like this won't work except in creation.
        classfile = yaml.safe_load(open('classes/' + key + '.yml').read())

    # Get skill points
    skill_points = cfunc.statmod(character_file["IQ"]) + classfile["skills per rank"]
    if "skilled" in character_file["specials"]:
        skill_points += 1
    x = 0
    skills = {}
    random.shuffle(class_skills)
    if skill_points <= 0:
        skill_points = 1
    while x < skill_points:
        # Get new class skills
        skills[class_skills.pop()] = 1
        # FIXME might get an error here with more skill points than skills
        # Pick random skills?  should never happen
        x += 1
    return skills


def pick_domains(domainlist):
    random.shuffle(domainlist)
    chosendomains = [domainlist.pop(), domainlist.pop()]
    return chosendomains


# Seems rather slow and clunking, will need optimizing
def yaml_create_character(char_race, char_class, mods="none", alignment='pick'):
    """
    Given a race and class, returns a yaml formatted character sheet.
    mods should be given as a list if any are desired.
    alignment should be in the 'CG' style or 'pick'. other inputs could be stupid.
    """
    genders = ["m", "f"]
    gender = random.choice(genders)
    name = fg.gen_name(gender, char_race)
    char_sheet = yaml.safe_load("name: " + name + "\n")
    char_sheet["gender"] = gender
    char_sheet["race"] = char_race
    # char_sheet[ "symbol: " + fg.coatofarms_gen() + "\n"
    interclassfile = {char_class: 1}
    char_sheet["class"] = interclassfile
    initstats = kind_stat_roll(char_class)
    
    ## Open the needed files and make sure they work before we go farther
    ## Should probably, at some point, move these to a database access system.

    racefile = yaml.safe_load(open('races/' + char_race + '.yml').read())

    classfile = yaml.safe_load(open('classes/' + char_class + '.yml').read())

    char_sheet["base attack"] = classfile["level 1"]["baseattack"]

    ## Apply Racial Bonuses
    adstats = cfunc.apply_race_stats(initstats, racefile, classfile)
    ## Make sure all of the stat values are possible.
    a = 0
    stats = ["ST", "DX", "CN", "WS", "IQ", "CH"]
    for i in adstats:
        if i < 3:
            adstats[a] = 3
        else:
            pass
        char_sheet[stats[a]] = adstats[a]
        a += 1

    # check both race file and class file for their respective specials
    speclist = classfile["level 1"]["special"] + racefile["race specials"]
    char_sheet["specials"] = speclist
    char_sheet["size"] = racefile["size"]
    char_sheet["speed"] = racefile["speed"]
    char_sheet["skills"] = pick_init_skills(char_sheet, classfile["class skills"])
    char_sheet["feats"] = pick_feat(mods, char_sheet)
    
    ##
    ## this section could be chopped out and moved to the 'level up' function, since its just
    ## adding a level one of a class to an existing character. Or it could handle it here 
    ## since it is kind of unique handling at level one.  
    ## 
    
    char_sheet["total hp"] = classfile["hit die"] + cfunc.nstatmod(adstats[2])
    char_sheet["current hp"] = classfile["hit die"] + cfunc.nstatmod(adstats[2])

    char_sheet["saves"] = {"fort": classfile["level 1"]["fortsave"],
                           "reflex": classfile["level 1"]["refsave"],
                           "will": classfile["level 1"]["willsave"]}
    # char_sheet["fort save"] = classfile["level 1"]["fortsave"]
    # char_sheet["reflex save"] = classfile["level 1"]["refsave"]
    # char_sheet["will save"] = classfile["level 1"]["willsave"]
    if alignment == 'pick':
        alignment = fg.pick_alignment(list(classfile["alignment"]))
    char_sheet["alignment"] = alignment

    deity = str(fg.pick_deity(alignment))
    char_sheet["deity"] = deity

    # Looking at picking spells here, but writing the whole spell list would be a pain...
    if str(classfile["magic type"]) == "None":
        pass
    elif str(classfile["magic type"]) == "Arcane":
        char_sheet["spells known"] = classfile["level 1"]["spells known"]
        char_sheet["spells per day"] = classfile["level 1"]["spells per day"]
        char_sheet["spells per day"]["first"] += math.ceil(cfunc.statmod(char_sheet[classfile["magic stat"]])/4)

    elif str(classfile["magic type"]) == "Divine":
        char_sheet["spells per day"] = classfile["level 1"]["spells per day"]
        char_sheet["spells per day"]["first"] += math.ceil(cfunc.statmod(char_sheet[classfile["magic stat"]])/4)
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
