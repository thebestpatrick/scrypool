#!/usr/bin/python3.3

from charactercreator import yaml_create_character
import yaml

print(yaml.dump(yaml_create_character("human", "wizard"), default_flow_style=False))