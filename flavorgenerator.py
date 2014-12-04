#!/usr/bin/python3.3

from roll import roll 
import random
import yaml


def name_gen_eng(gender):
    """Generates a random and rather vanilla medieval english sounding name"""
    # http://www.infernaldreams.com/names/Europe/Medieval/England.htm
    male_names_common = ['Adam', 'Geoffrey', 'Gilbert', 'Henry', 'Hugh', 'John', 'Nicholas',
     'Peter', 'Ralf', 'Richard', 'Robert', 'Roger', 'Simon', 'Thomas', 'Walter', 'William']
    
    male_names_uncommon = [
        'Alard', 'Ademar', 'Adelard', 'Aldous', 'Alphonse', 'Ancel', 'Arnold',
        'Bardol', 'Bernard', 'Bartram', 'Botolf',
        'Charles', 'Clarenbald', 'Conrad', 'Curtis',
        'Diggory', 'Drogo', 'Droyn', 'Dreue',
        'Ernis', 'Ernisius', 'Eude', 'Edon','Everard',
        'Faramond', 'Ferand','Frank', 'Frederick', 'Fawkes', 'Foulque',
        'Gaillard', 'Gerald', 'Gerard', 'Gervase', 'Godfrey', 'Guy',
        'Hamett', 'Harvey', 'Henry', 'Herman', 'Hubert', 'Yngerame',
        'Lance', 'Louis', 'Louve', 'Manfred', 'Miles', 'Norman', 'Otto',
        'Percival', 'Randal', 'Raymond', 'Reynard', 'Sagard', 'Serlo', 'Talbot', 'Theodoric',
        'Wymond'
    ]
    
    lastnames = [
        'Smith', 'Cooper', 'Cook', 'Hill', 'Underhill', 'Wright', 'Taylor', 'Chapman', 'Barker',
        'Tanner', 'Fiddler', 'Puttock', 'Arkwright', 'Mason', 'Carpenter', 'Dymond', 'Armstrong',
        'Black', 'White', 'Green', 'Gray', 'Sykes', 'Attwood', 'Miller'
    ]
    
    female_names_common = [
        'Emma', 'Agnes' , 'Alice', 'Avice', 'Beatrice', 'Cecily', 'Isabella',
        'Joan', 'Juliana', 'Margery', 'Matilda', 'Rohesia'
    ]
    
    female_names_uncommon = [
        'Adelaide', 'Ada', 'Aubrey', 'Alice', 'Alison', 'Avelina', 'Eleanor',
        'Ella', 'Galiena', 'Giselle', 'Griselda', 'Matilda', 'Millicent', 'Yvonne', 'Elizabeth', 'Eva',
        'Gabella', 'Jacqueline', 'Sapphira', 'Tyffany', 'Bridget', 'Guinevere', 'Isolda', 'Alexandra',
        'Cassandra', 'Denise', 'Sibyl'
    ]
    
    # MALE NAMES
    if gender == 'm':
        # Roll 1d100 to see if you get a standard first name or not.
        if roll(1,100) <= 60:
            # standard first name
            firstname = random.choice(male_names_common)
        else:
            # unusual first name
            firstname = random.choice(male_names_uncommon)
    # FEMALE NAMES
    else:
        # Roll 1d100 to see if you get a standard first name or not.
        if roll(1,100) <= 60:
            # standard first name
            firstname = random.choice(female_names_common)
        else:
            # unusual first name
            firstname = random.choice(female_names_uncommon)
    # LAST NAMES
    if roll(1,100) <= 50:
        lastname = random.choice(lastnames)
    else:
        lastname = random.choice(male_names_uncommon)
        if roll(1,10) < 4:
            lastname = lastname + "son"
    fullname = firstname + " " + lastname
    return fullname


def gen_name(gender, race):
    """Returns a random name given gender and race"""
    try:
        all = yaml.safe_load(open('races/' + race + '.yml').read())
        male_names_common = all["male common names"]
        male_names_uncommon = all["male uncommon names"]
    
        lastnames = all["lastnames"]
    
        female_names_common = all["female common names"]
    
        female_names_uncommon = all["female uncommon names"]
    except:
        return '"Bob" Dobbs'
    
    # MALE NAMES
    if gender == 'm':
        # Roll 1d100 to see if you get a standard first name or not.
        if roll(1,100) <= 60:
            # standard first name
            firstname = random.choice(male_names_common)
        else:
            # unusual first name
            firstname = random.choice(male_names_uncommon)
    # FEMALE NAMES
    else:
        # Roll 1d100 to see if you get a standard first name or not.
        if roll(1,100) <= 60:
            # standard first name
            firstname = random.choice(female_names_common)
        else:
            # unusual first name
            firstname = random.choice(female_names_uncommon)
    
    # A quick section to make some first names stupid, like Eddard instead of Edward.
    if roll(1,10) <= 3:
        q = 0
        while True:
            leng = len(list(firstname))
            leng = roll(1, leng)
            cletters = 'bcdfghjklmnprstvwz'
            #print(leng)
            if list(firstname)[leng-1] in cletters:
                #print(list(firstname)[leng-1])
                firstname = firstname[:leng-1] + random.choice(list(cletters)) + firstname[leng:]
                break
            else:
                q += 1
                if q >= 100:
                    break
    if roll(1,10) <= 3:
        q = 0
        while True:
            leng = len(list(firstname))
            leng = roll(1, leng)
            cletters = 'aeiuy'
            #print(leng)
            if list(firstname)[leng-1] in cletters:
                #print(list(firstname)[leng-1])
                firstname = firstname[:leng-1] + random.choice(list(cletters)) + firstname[leng:]
                break
            else:
                q += 1
                if q >= 100:
                    break
    # LAST NAMES
    if roll(1,100) <= 50:
        lastname = random.choice(lastnames)
    else:
        lastname = random.choice(male_names_uncommon)
        if roll(1,10) < 4:
            lastname = lastname + random.choice(all["endings"])
    fullname = firstname + " " + lastname
    
    #fullname = "x" + fullname[roll(1,len(list(fullname))):]
    
    return fullname


def hair():
    """Returns a style and color of hair"""
    colors = ['brown', 'red', 'blonde', 'black', 'dirty blonde', 'jet black', 'white', 'grey']
    styles = ['wavey', 'long', 'greasy', 'straight', 'neat', 'curly']
    return random.choice(colors) + " " + random.choice(styles)


def coatofarms_gen():
    """Generates a random coat of arms"""
    # Should someday take some sort of seed value to modify it.
    attitudes = ['Rampant', 'Passant', 'Sejant', 'Couchant', 'Courant', 'Dormant', 'Salient', 'Statant', 'Sejant Erect']
    attitudemod = ['Guardant', 'Regardant']
    
    colors = ['Black', 'Silver', 'Gray', 'Green', 'Gold', 'Red', 'Orange', 'Blue', 'Purple', 'Sky-blue']
    
    animals = [
        'Dragon', 'Lion', 'Stag', 'Wolf', 'Griffon', 'Eagle', 'Hawk', 'Owl', 'Raven', 'Horse', 'Elephant',
        'Pegasus', 'Unicorn', 'Dog', 'Cockatrice', 'Snake', 'Pike', 'Trout', 'Kraken', 'Leopard', 'Bear', 'Boar'
    ]
    symbols = ['Oak', 'Aspen', 'River', 'Sword', 'Axe', 'Key', 'Crown', 'Wheat', 'Rose', 'Sun', 'Boat']
    
    divisions = ['Fess', 'Pale', 'Bend', 'Bend sinister', 'Saltire', 'Cross', 'Chevron', 'Pall']  # party per
    # divisionmods = ['Wavy', 'Indented', 'Engrailed', 'Invected', 'Nebuly', 'Embattled', 'Dovetailed', 'Potenty']
    
    bends = ['Bend', 'Bendlet', 'Baton', 'Riband', 'Bendy of Six', 'Bend Cotised']
    
    f = roll(1,10)
    
    if f <= 4:
        # Do an animal set up.
        animal = random.choice(animals)
        colour = random.choice(colors)
        attitude = random.choice(attitudes)
        if f <= 2:
            attitude = attitude + " " + random.choice(attitudemod)
        # Do background:
        e = roll(1,6)
        if e == 1:
            # Bend set up
            background = random.choice(colors) + " a " + random.choice(bends) + " on " + random.choice(colors)
        elif e == 2:
            # Divided.
            background = "party per " + random.choice(divisions) + " " + random.choice(colors) + " and " +\
            random.choice(colors)
        else:
            # Solid
            background = random.choice(colors)
        fullcoat = "a " + colour + " " + attitude + " " + animal + " on " + background

    elif f <= 8:
        # Do a bend set up.
        background = random.choice(colors) + " a " + random.choice(bends) + " " + random.choice(colors)
        fullcoat = background
    else:
        # Do a symbol set up
        symbol = random.choice(symbols)
        colour = random.choice(colors)
        attitude = random.choice(attitudes)
        if f <= 2:
            attitude += " " + random.choice(attitudemod)
        # Do background:
        e = roll(1,6)
        if e == 1:
            # Bend set up
            background = random.choice(colors) + " a " + random.choice(bends) + " " + random.choice(colors)
        elif e == 2:
            # Divided.
            background = "party per " + random.choice(divisions) + " " + random.choice(colors) + " and " +\
            random.choice(colors)
        else:
            # Solid
            background = random.choice(colors)
        
        fullcoat = "a " + colour + " " + symbol + " on " + background
    return fullcoat


def pick_deity(alignment):
    """Selects a deity for the character out of the deities.yml file."""
    align_grid = [['LG', 'NG', 'CG'],
                  ['LN', 'NN', 'CN'],
                  ['LE', 'NE', 'CE']]
    if alignment[1] == 'G':
        pr = [0,1]
    elif alignment[1] == 'E':
        pr = [1,2]
    else:
        pr = [0,1,2]

    if alignment[0] == 'L':
        pc = [0,1]
    elif alignment[0] == 'C':
        pc = [1,2]
    else:
        pc = [0,1,2]


    try:
        deitylist = yaml.safe_load(open('deities.yml').read())
        random.shuffle(deitylist)
    except:
        pass
    for entity in deitylist:
        # check if the alignment is within a step
        deity_align = entity["alignment"]

        for b in pr:
            for c in pc:
                if deity_align == align_grid[b][c]:
                    return entity["name"]
                else:
                    pass
    return None



def pick_alignment(range, prepicked=False):
    """Given restrictions in 'range', picks an alignment"""
    # Implement some kind of thing in character sheets to restrict alignments...
    # A list, first entry is law to chaos, second is good to evil.
    # If something can be anything except something then say non [letter], i.e.
    # If a class cannot be lawful, then in l2c, say "non L"
    # Might have to change this at some point if lists ever get out of order.
    l2cl = ['L', 'N', 'C']
    g2el = ['G', 'N', 'E']
    l2c = range.pop(0)
    g2e = range.pop(0)

    # This is a shitty thing.  There needs to be checking to make sure this is a valid alignment
    if prepicked is not False:
        return prepicked

    if 'non' in g2e:
        g2el.remove(g2e[4])
        g2e = random.choice(g2el)
    if 'non' in l2c:
        l2cl.remove(l2c[4])
        l2c = random.choice(l2cl)

    if l2c == "any" and g2e == "any":
        align = random.choice(l2cl) + random.choice(g2el)
        return align

    elif l2c == "any" and g2e != "any":
        align = random.choice(l2cl) + g2e
        return align

    elif l2c != "any" and g2e == "any":
        align = l2c + random.choice(g2el)
        return align

    else:
        return l2c + g2e