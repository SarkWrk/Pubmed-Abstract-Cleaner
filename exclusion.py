import os
import datetime
import re as regex

in_path = "out"
out_path = "wanted"

long_covid_names = ["long covid", "post.acute covid", "post.acute sars.cov", "post.acute.sequelae covid", "post.acute.sequelae sars.cov", "long.haul covid", "pcas", "pcs", "post.covid"] # This is regex
accepted_disease_terms = ["aids", "hiv", "diabetes", "immunocomprom.* ", "immunodef.* "] # This is regex
dt = datetime.datetime.now()
words_per_min = 120
characters_per_word = 5

accepted_articles = []
accepted_pmids = []
total_characters = 0

for filename in os.listdir(os.path.join(os.path.dirname(__file__), in_path)):
    if ".txt" in filename:
        continue

    with open(os.path.join(os.path.join(os.path.dirname(__file__), in_path), filename), 'r', encoding="UTF-8") as input_file:
        lines = input_file.readlines()
        abstract_index = 3
        
        line_index = 0
        for line in lines:
            if line_index == 0:
                line_index += 1
                continue

            abstract = ""

            data = line.split('","')
            pmid = data[1]

            try:
                abstract = data[abstract_index]
            except:
                pass

            passed_long_covid_check = False
            passed_accepted_disease_terms_check = False

            for re in long_covid_names:
                if regex.findall(re, abstract.casefold()):
                    passed_long_covid_check = True

            if passed_long_covid_check == False:
                continue

            for re in accepted_disease_terms:
                if regex.findall(re, abstract.casefold()):
                    passed_accepted_disease_terms_check = True

            if passed_accepted_disease_terms_check == False:
                continue

            if pmid in accepted_pmids:
                continue

            accepted_articles.append(line)
            accepted_pmids.append(pmid)
            total_characters += len(abstract)

            line_index += 1
    
with open(os.path.join(os.path.join(os.path.dirname(__file__), out_path), str(dt.year) + "-" + str(dt.month) + "-" + str(dt.day) + ".csv"), "w+", encoding="UTF-8") as output_file:
    output_file.write("Link,PMID,Title,Abstract,Authors\n")

with open(os.path.join(os.path.join(os.path.dirname(__file__), out_path), str(dt.year) + "-" + str(dt.month) + "-" + str(dt.day) + ".csv"), "a", encoding="UTF-8") as output_file:
    for line in accepted_articles:
        output_file.write(line)

print("estimated: {}min".format(round(total_characters/(words_per_min*characters_per_word))))