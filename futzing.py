#!/usr/bin/python3.3

from charactercreator import yaml_create_character
import yaml
import random
#a = yaml.load(open("classes/barbarian.yml"))
#b = yaml.load(open("races/human.yml"))
# For testing everything
print(yaml.dump(yaml_create_character("halfling", "monk"), default_flow_style=False))