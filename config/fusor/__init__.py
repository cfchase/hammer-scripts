import yaml
import os


with open(os.path.dirname(__file__) + "/fusor.yaml") as fusor_data:
    SETTINGS = yaml.load(fusor_data)
