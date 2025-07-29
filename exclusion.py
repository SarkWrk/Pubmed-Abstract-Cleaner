import os
import datetime
import re as regex

in_path = "out"
out_path = "wanted"

long_covid_names = ["long covid", "post.acute covid", "post.acute sars.cov", "long.haul covid", "pcas", "pcs"] # This is regex
accepted_disease_terms = ["aids", "hiv", "diabetes", "immunocomprom.* ", "immunodef.* "] # This is regex
dt = datetime.datetime.now()

for filename in os.listdir(os.path.join(os.path.dirname(__file__), in_path)):
    if ".txt" in filename:
        continue

    accepted_articles = []

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

            accepted_articles.append(line)

            line_index += 1
    
    with open(os.path.join(os.path.join(os.path.dirname(__file__), out_path), str(dt.year) + "-" + str(dt.month) + "-" + str(dt.day) + ".csv"), "w+", encoding="UTF-8") as output_file:
        output_file.write("Link,PMID,Title,Abstract,Authors\n")

    with open(os.path.join(os.path.join(os.path.dirname(__file__), out_path), str(dt.year) + "-" + str(dt.month) + "-" + str(dt.day) + ".csv"), "a", encoding="UTF-8") as output_file:
        for line in accepted_articles:
            output_file.write(line)