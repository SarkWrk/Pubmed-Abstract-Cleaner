import os
import json

# Run formatter.py
import modules.formatter

# Unique articles
unique_articles = []
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
    if "export.csv" in file_name:
        if log_level == "Debug":
            print("export.csv already exists in directory - skipping!")
        continue

    with open(os.path.join(os.path.join(correct_dir, output_path), file_name), "r", encoding="UTF-8") as data:
        if log_level == "Debug":
            print("Opening {}".format(file_name))

        lines = data.readlines()
        in_header = True

        pmid_section = 2

        for line in lines:
            if in_header == True:
                in_header = False
                continue
        
            split_line = line.split('","')

            pmid = split_line[pmid_section]

            if pmid in unique_pmids:
                total_duplicate_articles += 1
                continue
            else:
                unique_pmids.add(pmid)
                unique_articles.append(line)

with open(os.path.join(os.path.join(correct_dir, output_path), "export.csv"), "w+", encoding="UTF-8") as export_file:
    export_file.write("Link,PMID,Title,Abstract,Authors\n")

    for article in unique_articles:
        export_file.write(article)
    
print("Removed {} duplicate articles.".format(total_duplicate_articles))