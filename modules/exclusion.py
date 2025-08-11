import os
import json
import datetime
import re as regex

# Remove duplicates
import modules.duplicate_remover

# Relative paths for file locations
input_path = ""
output_path = ""

# Filter terms
long_covid_names = [] # This is regex
accepted_disease_terms = [] # This is regex

# This is used to title the output .csv file
dt = datetime.datetime.now()

# Estimated read time params
words_per_min = 120
characters_per_word = 5

# List of articles to be put in the output .csv file
accepted_articles = []

# Character count stuff for estimate
total_characters = 0

# Dirname
correct_dir = os.path.dirname(os.path.dirname(__file__))

# Log level
log_level = ""

with open(os.path.join(os.path.join(correct_dir, "settings"), "settings.json"), "r") as settings_file:
    settings_string = settings_file.read()
    settings = json.loads(settings_string)
    
    input_path = settings["paths"]["output"]
    output_path = settings["paths"]["wanted"]

    log_level = settings["log_level"]

    exclusion_criteria = settings["exclusion_criteria"]

    for criteria in exclusion_criteria["long_covid_names"]:
        long_covid_names.append(criteria.replace("\\\\", "\\"))

    for criteria in exclusion_criteria["accepted_disease_terms"]:
        accepted_disease_terms.append(criteria.replace("\\\\", "\\"))

with open(os.path.join(os.path.join(correct_dir, input_path), "export.csv"), 'r', encoding="UTF-8") as input_file:
    lines = input_file.readlines()
    abstract_index = 3
    
    line_index = 0
    for line in lines:
        if line_index == 0:
            line_index += 1
            continue

        abstract = ""

        data = line.split('","')
        
        try:
            pmid = data[1]
        except:
            if log_level == ("Errors" or "Debug"):
                print("Couldn't find the PMID in line {}. Data: {}".format(line_index, data))


        try:
            abstract = data[abstract_index]
        except:
            pass

        # Article filtering starts here

        passed_long_covid_check = False
        passed_accepted_disease_terms_check = False

        for re in long_covid_names:
            found_in = regex.findall(" " + re + " ", abstract.casefold())
            if found_in:
                # PCS can also mean physical component score
                if re == ("pcs" or "pasc" or "pacs"):
                    if not regex.findall(" covid.?\d* ", abstract.casefold()):
                        continue
                passed_long_covid_check = True

        if passed_long_covid_check == False:
            continue

        for re in accepted_disease_terms:
            found_in = regex.findall(" " + re + " ", abstract.casefold())
            if found_in:
                passed_accepted_disease_terms_check = True

        if passed_accepted_disease_terms_check == False:
            continue

        # Article filtering ends here

        # Append to list, prevent repeat pmids, character count for estimate
        accepted_articles.append(line)
        total_characters += len(abstract)

        line_index += 1
    
# Write to file
with open(os.path.join(os.path.join(correct_dir, output_path), str(dt.year) + "-" + str(dt.month) + "-" + str(dt.day) + ".csv"), "w+", encoding="UTF-8") as output_file:
    output_file.write("Link,PMID,Title,Abstract,Authors\n")

    for line in accepted_articles:
        output_file.write(line)

print("Estimated: {}min".format(round(total_characters/(words_per_min*characters_per_word))))