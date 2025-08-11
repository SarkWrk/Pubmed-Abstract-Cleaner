import os
import json

paths = []

dirname = os.path.dirname(__file__)

with open(os.path.join(os.path.join(dirname, "settings"), "settings.json"), "r") as settings_file:
    settings = json.loads(settings_file.read())
    paths = settings["paths"]

for path_category in paths:
    if os.path.exists(os.path.join(dirname, paths[path_category])):
        continue

    os.makedirs(os.path.join(dirname, paths[path_category]))

import modules.exclusion

print("Finished running!")