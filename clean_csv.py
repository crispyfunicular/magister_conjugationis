from project import *

def save_verbs(output, verbs):
    """
    *Input* (two)
    output (str) = the file name of the clean csv
    verbs (list of dict) = the verbs loaded and cleaned by get_verbs()
    """
    headers = "infinitive;infinitif;group;voice;tense;person;latin;french;primitive tenses"
    column_names = headers.split(";")

    with open(output, "w", encoding="utf-8-sig") as f:

        # Write the first line with the column headers
        f.write(f"{headers}\n")

        for verb in verbs:
            columns = []
            for column_name in column_names:
                column_value = str(verb[column_name])
                columns.append(column_value)

            line = ";".join(columns)
            f.write(f"{line}\n")

def main():
    """
    This program loads a CSV file, cleans it (v->u, j->i) and saves it
    """
    input = "verbs_latin.csv"
    output = "verbs_latin_ok.csv"

    ###
    # Load and clean the dirty CSV file
    ###

    verbs = get_verbs(input)

    ###
    # Save the clean CSV file
    ###

    save_verbs(output, verbs)

if __name__ == "__main__":
    main()
