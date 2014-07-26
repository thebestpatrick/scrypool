#!/bin/python3.3

from charactercreator import yaml_create_character
import yaml

#a = yaml.load(open("classes/barbarian.yml"))
#b = yaml.load(open("races/human.yml"))
#speclist = a["level 1"]["special"] + b["race specials"]
#print(parse_specials(speclist))
print(yaml.dump(yaml_create_character("human", "barbarian", "null"), default_flow_style=False))