#!/usr/bin/python3.3

from charactercreator import yaml_create_character
import yaml
#a = yaml.load(open("classes/barbarian.yml"))
#b = yaml.load(open("races/human.yml"))

print(yaml.dump(yaml_create_character("elf", "barbarian", ["mobility", ]), default_flow_style=False))

