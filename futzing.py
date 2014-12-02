#!/usr/bin/python3.3

from charactercreator import yaml_create_character
import yaml
import random
#a = yaml.load(open("classes/barbarian.yml"))
#b = yaml.load(open("races/human.yml"))
# For testing everything
print(yaml.dump(yaml_create_character("human", "fighter"), default_flow_style=False))

"""character_file = ['fighter bonus feat', 'bonus feat', 'skilled']
for s in character_file:
    print(s)
    if s == 'bonus feat':
        print("fuck")

    elif s == 'fighter bonus feat':
        print("well that works")

    else:
        pass"""