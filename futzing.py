#!/bin/python3.3

from charactercreator import yaml_create_character
import yaml
a = yaml_create_character("human", "barbarian", "none")
f = open("charactersheets/blah.yml", 'w')
f.write(a)