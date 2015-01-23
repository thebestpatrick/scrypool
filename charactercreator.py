#!/usr/bin/python3.3

import yaml
import math
import cfunc
import roll
import random

import flavorgenerator as fg


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
        # moved all but the first entry here in to this loop.  Not sure why they were out of
        # the loop, but maybe there was a reason.  In any case, they are in now, so any odd errors
        # might be traced to here I guess.
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


def apply_bloodline(character_file):
    """
    Does the initial simple application of a bloodline file to a sorcerer's character sheet.
    """
    bloodfile = yaml.safe_load(open('classes/misc/bloodlines.yml').read())
    # Choose a bloodline

    # add that bloodline to the character file
    # Add the bonus class skills to an appropriate field.
    #


def parse_specials(character_file):
    """
    A function for taking race and class special features, like bonus feat and domains,
    and turning them into the thing that they mean, then returning the proper list of specials.
    """
    deadlist = []
    mods = []  # probably add a section that can allow people to add tags to their character sheet
    for s in character_file["specials"]:
        if isinstance(s, list):
            alpha = random.choice(s)
            deadlist += [s, ]
            character_file["specials"].append(alpha)
            # parse_specials(character_file)

        elif isinstance(s, dict):  # NOTE: dicts in class file specials will be processed as such
            deadlist += [s, ]
            for key, value in s.items():
                character_file["specials"] += [key, ]
                mods += [value, ]

        if s == "bonus feat":
            # pick a generic bonus feat
            deadlist += [s, ]
            character_file["feats"] += pick_feat(mods, character_file)  # FIXME maybe get tags arg 1?

        elif s == "fighter bonus feat":
            # pick a fighter bonus feat
            deadlist += [s, ]
            character_file["feats"] += pick_feat(["fighter bonus", ], character_file)

        elif s == "domains":
            deadlist += [s, ]
            deities = yaml.safe_load(open('deities.yml').read())
            domains = ["failure", "unusual errors"]
            for zzz in deities:
                if zzz["name"] == character_file["deity"]:
                    domains = pick_domains(zzz["domains"])
                    break
                else:
                    pass
            character_file["domains"] = domains

        elif s == "favored enemy":  # This favored enemy stuff should be useful later for rogue talents
            # and even the ranger weapon tree.
            deadlist += [s,]
            # Get what is there.  if there is one, add to it.
            try:
                current_favored_enemy_info = character_file["favored enemies"]
                random.shuffle(current_favored_enemy_info)
                for anenemy in current_favored_enemy_info:
                    for key, value in anenemy.items():
                        current_favored_enemy_info[0][key] += 2
                        break
                break
            except:
                current_favored_enemy_info = {}
                character_file["favored enemies"] = []
            # open file and pick one
            enemies = yaml.safe_load(open('classes/misc/favored enemies.yml').read())
            for e in enemies:
                enemy = random.choice(enemies)
                # make sure it hasn't been picked before
                if enemy in current_favored_enemy_info:
                    # FIXME: THIS PART IS ALL FUCKED UP....WORK ON IT
                    pass
                else:
                    # apply it
                    character_file["favored enemies"] += [{enemy: 2}]
                    break

        # no need to have a bunch of smite 1, smite 2 hanging around
        # elif isinstance(s[-1], int) and s[:-2] in character_file["specials"]:
            # deadlist += [s, ]
        elif s == "bloodline power":
            # FIXME: needing bloodline handling in general.  Also, all the wizard bullshit
            pass
        else:
            # stuff
            continue  # doing nothing I guess?
    for bullet in deadlist:
        character_file["specials"].remove(bullet)
    return character_file


def pick_init_skills(character_file, class_skills):
    """
    Picks out a suite of skills from class skills and adds them to character file in form skill: 1
    Only useful during character creation, really this should all get the same treatment of feats...
    but that sounds hard, and no one cares about skills anyway.
    """
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
    """
    Picks two random domains from a list and returns a list of them.
    really, converts any list into a list with two random items
    """
    random.shuffle(domainlist)
    chosendomains = [domainlist.pop(), domainlist.pop()]
    return chosendomains


# Seems rather slow and clunking, will need optimizing
# would take some work, but running the whole thing as a class might be viable.
# Might speed it up with 'self' references instead of tossing text blobs around.
def yaml_create_character(char_race, char_class, mods='none', alignment='pick'):
    """
    Given a race and class, returns a yaml formatted character sheet.
    mods should be given as a list if any are desired.
    alignment should be in the 'CG' style or 'pick'. other inputs WILL be stupid.
    """
    genders = ["m", "f"]
    gender = random.choice(genders)
    name = fg.gen_name(gender, char_race)
    char_sheet = yaml.safe_load("name: " + name + "\n")
    char_sheet["gender"] = gender
    char_sheet["race"] = char_race

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
    char_sheet["base speed"] = racefile["speed"]
    char_sheet["skills"] = pick_init_skills(char_sheet, classfile["class skills"])

    # should probably add weapon proficiencies in at this point too.
    # this will require adding them to the class sheets.
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
    if alignment == 'pick':
        alignment = fg.pick_alignment(list(classfile["alignment"]))
    else:
        alignment = fg.pick_alignment(list(classfile["alignment"]), alignment)
    char_sheet["alignment"] = alignment

    deity = str(fg.pick_deity(alignment))
    char_sheet["deity"] = deity

    # Looking at picking spells here, but writing the whole spell list would be a pain...
    if str(classfile["magic type"]) == "None":
        pass
    elif str(classfile["magic type"]) == "Arcane":
        char_sheet["spells known"] = classfile["level 1"]["spells known"]
        char_sheet["spells per day"] = classfile["level 1"]["spells per day"]
        try:
            char_sheet["spells per day"]["1"] += math.ceil(cfunc.statmod(char_sheet[classfile["magic stat"]])/4)
        except:
            pass

    elif str(classfile["magic type"]) == "Divine":
        char_sheet["spells per day"] = classfile["level 1"]["spells per day"]
        try:  # Try it, because some casters don't have first level spells at first.
            char_sheet["spells per day"]["1"] += math.ceil(cfunc.statmod(char_sheet[classfile["magic stat"]])/4)
        except:
            pass
    else:
        pass
        # Might be tricky, but handle this oddity some other way

    # Pass the string in for post processing, things like feat assignment and some 
    # parsing work regarding it.
    char_sheet = parse_specials(char_sheet)

    return char_sheet
