import os
import json
import re as regex

# Relative paths for file locations
input_path = ""
output_path = ""

# Set of keywords to ignore
ignored_lines = ["PMCID:", "DOI:"]

# Dirname
correct_dir = os.path.dirname(os.path.dirname(__file__))

# Log level
log_level = ""

with open(os.path.join(os.path.join(correct_dir, "settings"), "settings.json"), "r") as settings_file:
    settings_string = settings_file.read()
    settings = json.loads(settings_string)

    log_level = settings["log_level"]
    
    input_path = settings["paths"]["input"]
    output_path = settings["paths"]["output"]

for filename in os.listdir(os.path.join(correct_dir, input_path)):
    with open(os.path.join(os.path.join(correct_dir, input_path), filename), 'r', encoding="UTF-8") as input_file:
        print("Parsing {}".format(filename))

        in_title = False
        in_auth_info = False
        in_erratum = False
        in_collaborators = False
        in_conf_of_int = False
        in_copyright = False
        in_comments = False
        in_updates = False

        formatted_text = ""

        # Removing useless stuff that we don't care about
        for line in input_file.readlines():
            cleaned_line = line #line.strip()

            # Ignore specific keywords
            if any(ignored_line in cleaned_line for ignored_line in ignored_lines):
                continue

            # Ignore the article number
            if regex.search("^\d+\. ", cleaned_line) and regex.search(";\d", cleaned_line):
                in_title = True
                continue

            # Ignore author information section
            if "Author information:" in cleaned_line:
                in_auth_info = True
                continue

            # Ignore erratums
            if "Erratum in" in cleaned_line:
                in_erratum = True
                continue

            # Ignore collaborator section
            if "Collaborators:" in cleaned_line:
                in_collaborators = True
                continue

            # Ignore conflict of interest section
            if "Conflict of interest statement:" in cleaned_line:
                in_conf_of_int = True
                continue

            # Ignore copyright secton
            if "©" in cleaned_line:
                in_copyright = True
                continue

            # Ignore comment section
            if regex.search("^Comment .n", cleaned_line):
                in_comments = True
                continue

            # Ignore update section
            if regex.search("^Update of", cleaned_line) or regex.search("^Update in", cleaned_line):
                in_updates = True
                continue

            # Newline means that it's a new section
            if cleaned_line == ("" or "\n"):
                in_title = False
                in_auth_info = False
                in_erratum = False
                in_collaborators = False
                in_conf_of_int = False
                in_copyright = False
                in_comments = False
                in_updates = False

            # Skip the sections we don't care about
            if (in_auth_info or in_erratum or in_collaborators or in_conf_of_int or in_title or in_copyright or in_comments or in_updates) == True:
                continue

            formatted_text += cleaned_line

        # Format the text to look prettier
        new_text = ""

        split_lines = formatted_text.splitlines()
        inc = 0

        next_line = ""

        # Rewrite 
        for line in split_lines:
            if inc == len(split_lines) - 1:
                next_line == ""
            else:
                next_line = split_lines[inc + 1]
            inc += 1

            if line == "" and next_line == "":
                continue

            if line == "":
                new_text += "\n"
            else:
                new_text += line

        if log_level == "Debug":
            print("Prepared text file for csv formatting")

        # Write in csv format
        headers = ["Title", "Authors", "Abstract", "PMID", "Link"]
        link_starter = "https://pubmed.ncbi.nlm.nih.gov/"

        header = "Link,PMID,Title,Abstract,Authors"

        # Create new lines for csv format
        articles = {0: {}}

        split_output = new_text.splitlines()

        inc = 0
        new_subdict = 0
        create_new_subgroup = False

        for data in split_output:
            if data == "":
                continue

            if "PMID:" in data:
                create_new_subgroup = True

                pmid = regex.findall("\d+", data)
                if not pmid:
                    articles[new_subdict]["PMID"] = ""
                else:
                    articles[new_subdict]["PMID"] = pmid[0]
                continue

            if create_new_subgroup == True:
                create_new_subgroup = False

                new_subdict += 1
                inc = 0
                articles[new_subdict] = {}

            try:
                if headers[inc] == "PMID":
                    continue

                articles[new_subdict][headers[inc]] = data.replace('"', "''")
            except:
                pass
            
            inc += 1

        for subdict in articles:
            dict = articles[subdict]
            try:
                dict["Link"] = link_starter + dict["PMID"]
            except:
                print(dict)

                dict["Link"] = ""

            # FIx empty fields
            try:
                if dict["PMID"]:
                    pass
            except:
                dict["PMID"] = ""

            try:
                if dict["Title"]:
                    pass
            except:
                dict["Title"] = ""

            try:
                if dict["Abstract"]:
                    pass
            except:
                dict["Abstract"] = ""

            try:
                if dict["Author"]:
                    pass
            except:
                dict["Author"] = ""

        new_file_name = filename.replace(".txt", ".csv")

        # Write results to disk
        with open(os.path.join(os.path.join(correct_dir, output_path), new_file_name), 'w+', encoding="UTF-8") as output_csv:
            if log_level == "Debug":
                print("Writing {} to disk".format(new_file_name))

            output_csv.write(header + "\n")

            for subdicts in articles:
                dict = articles[subdicts]
                try:
                    output_csv.write('"' + dict["Link"] + '"' + "," + '"' + dict["PMID"] + '"' + "," + '"' + dict["Title"] + '"' + "," + '"' + dict["Abstract"] + '"' + "," + '"' + dict["Authors"] + '"' + "\n")
                except:
                    if log_level == ("Errors" or "Debug"):
                        print("Errored trying to write an entry to {}!\nData: {}".format(new_file_name, dict))