#!/usr/bin/python3.3

from roll import roll 
import random
import yaml
import string

def name_gen_eng(gender): ## Generates a random and rather vanilla medieval english sounding name
    # http://www.infernaldreams.com/names/Europe/Medieval/England.htm
    male_names_common = ['Adam', 'Geoffrey', 'Gilbert', 'Henry', 'Hugh', 'John', 'Nicholas',\
     'Peter', 'Ralf', 'Richard', 'Robert', 'Roger', 'Simon', 'Thomas', 'Walter', 'William']
    
    male_names_uncommon = ['Alard', 'Ademar', 'Adelard', 'Aldous', 'Alphonse', 'Ancel', 'Arnold', \
    'Bardol', 'Bernard', 'Bartram', 'Botolf',\
    'Charles', 'Clarenbald', 'Conrad', 'Curtis',\
    'Diggory', 'Drogo', 'Droyn', 'Dreue',\
    'Ernis', 'Ernisius', 'Eude', 'Edon','Everard',\
    'Faramond', 'Ferand','Frank', 'Frederick', 'Fawkes', 'Foulque',\
    'Gaillard', 'Gerald', 'Gerard', 'Gervase', 'Godfrey', 'Guy',\
    'Hamett', 'Harvey', 'Henry', 'Herman', 'Hubert', 'Yngerame',\
    'Lance', 'Louis', 'Louve', 'Manfred', 'Miles', 'Norman', 'Otto',\
    'Percival', 'Randal', 'Raymond', 'Reynard', 'Sagard', 'Serlo', 'Talbot', 'Theodoric',\
    'Wymond']
    
    lastnames = ['Smith', 'Cooper', 'Cook', 'Hill', 'Underhill', 'Wright', 'Taylor', 'Chapman', 'Barker',\
    'Tanner', 'Fiddler', 'Puttock', 'Arkwright', 'Mason', 'Carpenter', 'Dymond', 'Armstrong',\
    'Black', 'White', 'Green', 'Gray', 'Sykes', 'Attwood', 'Miller']
    
    female_names_common = ['Emma', 'Agnes' , 'Alice', 'Avice', 'Beatrice', 'Cecily', 'Isabella',\
    'Joan', 'Juliana', 'Margery', 'Matilda', 'Rohesia']
    
    female_names_uncommon = ['Adelaide', 'Ada', 'Aubrey', 'Alice', 'Alison', 'Avelina', 'Eleanor',\
    'Ella', 'Galiena', 'Giselle', 'Griselda', 'Matilda', 'Millicent', 'Yvonne', 'Elizabeth', 'Eva',\
    'Gabella', 'Jacqueline', 'Sapphira', 'Tyffany', 'Bridget', 'Guinevere', 'Isolda', 'Alexandra',\
    'Cassandra', 'Denise', 'Sibyl']
    
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
    try:
        all = yaml.load(open('races/' + race + '.yml').read())
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

## Hair color and style
def hair(): # might want to allow input on this
    colors = ['brown', 'red', 'blonde', 'black', 'dirty blonde', 'jet black', 'white', 'grey']
    styles = ['wavey', 'long', 'greasy', 'straight', 'neat', 'curly']
    return random.choice(colors) + " " + random.choice(styles)

def coatofarms_gen(): ## Generates a random coat of arms
    # Should someday take some sort of seed value to modify it.
    attitudes = ['Rampant', 'Passant', 'Sejant', 'Couchant', 'Courant', 'Dormant', 'Salient', 'Statant', 'Sejant Erect']
    attitudemod = ['Guardant', 'Regardant']
    
    colors = ['Black', 'Silver', 'Gray', 'Green', 'Gold', 'Red', 'Orange', 'Blue', 'Purple', 'Sky-blue']
    
    animals = ['Dragon', 'Lion', 'Stag', 'Wolf', 'Griffon', 'Eagle', 'Hawk', 'Owl', 'Raven', 'Horse', 'Elephant',\
    'Pegasus', 'Unicorn', 'Dog', 'Cockatrice', 'Snake', 'Pike', 'Trout', 'Kraken', 'Leopard', 'Bear', 'Boar']
    symbols = ['Oak', 'Aspen', 'River', 'Sword', 'Axe', 'Key', 'Crown', 'Wheat', 'Rose', 'Sun', 'Boat']
    
    divisions = ['Fess', 'Pale', 'Bend', 'Bend sinister', 'Saltire', 'Cross', 'Chevron', 'Pall'] # party per
    divisionmods = ['Wavy', 'Indented', 'Engrailed', 'Invected', 'Nebuly', 'Embattled', 'Dovetailed', 'Potenty']
    
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
        if f <= 2:
            attitude = attitude + " " + random.choice(attitudemod)
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

#def generic_tavern_generator(): ## Generate a generic tavern layout and occupants
    # Should also someday take modifiers to affect its behavior.

#def generic_castle_generator(size, culture): ## Generate a fort or castle based on parameters
    # Size is pretty standard, but culture could be like viking, crusader, anything really
    # Might need its own file. 

#def generic_building_generator(culture): ## Generate a quick building of a random type, with contents.
    # Culture could be urban, rural, viking, elf, anything.
    # This one might need its own file too

#for x in range(1,10):
    #print(name_gen_eng('m') + "'s coat of arms is " + coatofarms_gen())