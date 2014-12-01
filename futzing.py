#!/usr/bin/python3.3

from charactercreator import yaml_create_character
import yaml
#a = yaml.load(open("classes/barbarian.yml"))
#b = yaml.load(open("races/human.yml"))
# For testing everything
print(yaml.dump(yaml_create_character("halfling", "bard"), default_flow_style=False))

# Testing alignment
#import flavorgenerator as fg
#print(fg.pick_alignment(["L", "any"]))
