import os
import json

# Run formatter.py
import modules.formatter

# Unique articles
unique_articles = {}
unique_pmids = set()

# Total duplicate articles
total_duplicate_articles = 0

# Dirname
correct_dir = os.path.dirname(os.path.dirname(__file__))

# File path
output_path = ""

# Log level
log_level = ""

with open(os.path.join(os.path.join(correct_dir, "settings"), "settings.json"), "r") as settings_file:
    settings_string = settings_file.read()
    settings = json.loads(settings_string)

    log_level = settings["log_level"]
    
    output_path = settings["paths"]["output"]

for file_name in os.listdir(os.path.join(correct_dir, output_path)):
    if "export.json" in file_name:
        if log_level == "Debug":
            print("export.json already exists in directory - skipping!")
        continue

    with open(os.path.join(os.path.join(correct_dir, output_path), file_name), "r", encoding="UTF-8") as data:
        if log_level == "Debug":
            print("Opening {}".format(file_name))

        lines = json.loads(data.read())

        for line in lines:
            data = lines[line]
            pmid = data["PMID"]

            if pmid in unique_pmids:
                total_duplicate_articles += 1
                continue
            else:
                unique_pmids.add(pmid)
                unique_articles[pmid] = data

with open(os.path.join(os.path.join(correct_dir, output_path), "export.json"), "w+", encoding="UTF-8") as export_file:
    output_string = json.dumps(unique_articles, indent=4, ensure_ascii=False, sort_keys=True)
    export_file.write(output_string)
    
print("Removed {} duplicate articles.".format(total_duplicate_articles))