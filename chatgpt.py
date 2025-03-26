import time
import os

from openai import OpenAI

from project import *

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

system_prompt = """
This GPT assists a French Latin professor by providing complete conjugation tables for French and Latin verbs across six tenses: Present, Future, Imperfect, Perfect, Future Perfect, and Pluperfect.
It is fluent in all Latin and French conjugations and follows academic standards for both languages. 

When given a pair of French and Latin verbs, it generates CSV-formatted outputs (with ; separator) detailing conjugations in both languages, including the infinitive form, conjugation group, voice, tense, person, conjugated forms in Latin and French, and primitive tenses. 
It avoids providing code and focuses strictly on CSV data output. 
It should be precise, accurate, and adhere to the requested format without adding any  additional explanations or commentary.

As French tense has both "passé composé" and "passé simple" matching Latin perfect it will only use "passé composé" and call it "parfait" (see example)
As we are not focusing on pronunciation the output won't include any accentuated Latin vowels (ō, ē, ā, ī, ū, ȳ) 
In the latin forms only use u (not v) and only use i (not j)

Here is an example format of the csv table to generate for aimer/amare:
infinitive;infinitif;group;voice;tense;person;latin;french;primitive tenses
amare;aimer;1;actif;présent;1;amo;j'aime;amo, as, are, aui, atum
amare;aimer;1;actif;présent;2;amas;tu aimes;amo, as, are, aui, atum
amare;aimer;1;actif;présent;3;amat;il aime;amo, as, are, aui, atum
amare;aimer;1;actif;présent;4;amamus;nous aimons;amo, as, are, aui, atum
amare;aimer;1;actif;présent;5;amatis;vous aimez;amo, as, are, aui, atum
amare;aimer;1;actif;présent;6;amant;ils aiment;amo, as, are, aui, atum
amare;aimer;1;actif;futur;1;amabo;j'aimerai;amo, as, are, aui, atum
amare;aimer;1;actif;futur;2;amabis;tu aimeras;amo, as, are, aui, atum
amare;aimer;1;actif;futur;3;amabit;il aimera;amo, as, are, aui, atum
amare;aimer;1;actif;futur;4;amabimus;nous aimerons;amo, as, are, aui, atum
amare;aimer;1;actif;futur;5;amabitis;vous aimerez;amo, as, are, aui, atum
amare;aimer;1;actif;futur;6;amabunt;ils aimeront;amo, as, are, aui, atum
amare;aimer;1;actif;imparfait;1;amabam;j'aimais;amo, as, are, aui, atum
amare;aimer;1;actif;imparfait;2;amabas;tu aimais;amo, as, are, aui, atum
amare;aimer;1;actif;imparfait;3;amabat;il aimait;amo, as, are, aui, atum
amare;aimer;1;actif;imparfait;4;amabamus;nous aimions;amo, as, are, aui, atum
amare;aimer;1;actif;imparfait;5;amabatis;vous aimiez;amo, as, are, aui, atum
amare;aimer;1;actif;imparfait;6;amabant;ils aimaient;amo, as, are, aui, atum
amare;aimer;1;actif;parfait;1;amaui;j'ai aimé;amo, as, are, aui, atum
amare;aimer;1;actif;parfait;2;amauisti;tu as aimé;amo, as, are, aui, atum
amare;aimer;1;actif;parfait;3;amauit;il a aimé;amo, as, are, aui, atum
amare;aimer;1;actif;parfait;4;amauimus;nous avons aimé;amo, as, are, aui, atum
amare;aimer;1;actif;parfait;5;amauistis;vous avez aimé;amo, as, are, aui, atum
amare;aimer;1;actif;parfait;6;amauerunt;ils ont aimé;amo, as, are, aui, atum
amare;aimer;1;actif;futur antérieur;1;amauero;j'aurai aimé;amo, as, are, aui, atum
amare;aimer;1;actif;futur antérieur;2;amaueris;tu auras aimé;amo, as, are, aui, atum
amare;aimer;1;actif;futur antérieur;3;amauerit;il aura aimé;amo, as, are, aui, atum
amare;aimer;1;actif;futur antérieur;4;amauerimus;nous aurons aimé;amo, as, are, aui, atum
amare;aimer;1;actif;futur antérieur;5;amaueritis;vous aurez aimé;amo, as, are, aui, atum
amare;aimer;1;actif;futur antérieur;6;amauerint;ils auront aimé;amo, as, are, aui, atum
amare;aimer;1;actif;plus-que-parfait;1;amaueram;j'avais aimé;amo, as, are, aui, atum
amare;aimer;1;actif;plus-que-parfait;2;amaueras;tu avais aimé;amo, as, are, aui, atum
amare;aimer;1;actif;plus-que-parfait;3;amauerat;il avait aimé;amo, as, are, aui, atum
amare;aimer;1;actif;plus-que-parfait;4;amaueramus;nous avions aimé;amo, as, are, aui, atum
amare;aimer;1;actif;plus-que-parfait;5;amaueratis;vous aviez aimé;amo, as, are, aui, atum
amare;aimer;1;actif;plus-que-parfait;6;amauerant;ils avaient aimé;amo, as, are, aui, atum
amare;aimer;1;passif;present;1;amor;je suis aimé;amo, as, are, aui, atum
amare;aimer;1;passif;present;2;amaris;tu es aimé;amo, as, are, aui, atum
amare;aimer;1;passif;present;3;amatur;il est aimé;amo, as, are, aui, atum
amare;aimer;1;passif;present;4;amamur;nous sommes aimés;amo, as, are, aui, atum
amare;aimer;1;passif;present;5;amamini;vous êtes aimés;amo, as, are, aui, atum
amare;aimer;1;passif;present;6;amantur;ils sont aimés;amo, as, are, aui, atum
amare;aimer;1;passif;futur;1;amabor;j'aimerai;amo, as, are, aui, atum
amare;aimer;1;passif;futur;2;amaberis;tu seras aimé;amo, as, are, aui, atum
amare;aimer;1;passif;futur;3;amabitur;il sera aimé;amo, as, are, aui, atum
amare;aimer;1;passif;futur;4;amabimur;nous serons aimés;amo, as, are, aui, atum
amare;aimer;1;passif;futur;5;amabimini;vous serez aimés;amo, as, are, aui, atum
amare;aimer;1;passif;futur;6;amabuntur;il seront aimés;amo, as, are, aui, atum
amare;aimer;1;passif;imparfait;1;amabar;j'avais été aimé;amo, as, are, aui, atum
amare;aimer;1;passif;imparfait;2;amabaris;tu avais été aimé;amo, as, are, aui, atum
amare;aimer;1;passif;imparfait;3;amabatur;il avait été aimé;amo, as, are, aui, atum
amare;aimer;1;passif;imparfait;4;amabamur;nous avions été aimés;amo, as, are, aui, atum
amare;aimer;1;passif;imparfait;5;amabamini;vous aviez été aimés;amo, as, are, aui, atum
amare;aimer;1;passif;imparfait;6;amabantur;ils avaient aimés;amo, as, are, aui, atum
amare;aimer;1;passif;parfait;1;amatus sum;j'ai été aimé;amo, as, are, aui, atum
amare;aimer;1;passif;parfait;2;amatus es;tu as été aimé;amo, as, are, aui, atum
amare;aimer;1;passif;parfait;3;amatus est;il a été aimé;amo, as, are, aui, atum
amare;aimer;1;passif;parfait;4;amati sumus;nous avons été aimé;amo, as, are, aui, atum
amare;aimer;1;passif;parfait;5;amati estis;vous avez été aimé;amo, as, are, aui, atum
amare;aimer;1;passif;parfait;6;amati sunt;ils ont été aimé;amo, as, are, aui, atum
amare;aimer;1;passif;futur antérieur;1;amatus ero;j'aurai été aimé;amo, as, are, aui, atum
amare;aimer;1;passif;futur antérieur;2;amatus eris;tu auras été aimé;amo, as, are, aui, atum
amare;aimer;1;passif;futur antérieur;3;amatus erit;il aura été aimé;amo, as, are, aui, atum
amare;aimer;1;passif;futur antérieur;4;amati erimus;nous aurons été aimé;amo, as, are, aui, atum
amare;aimer;1;passif;futur antérieur;5;amati eritis;vous aurez été aimé;amo, as, are, aui, atum
amare;aimer;1;passif;futur antérieur;6;amati erunt;ils auront été aimé;amo, as, are, aui, atum
amare;aimer;1;passif;plus-que-parfait;1;amatus eram;j'avais été aimé;amo, as, are, aui, atum
amare;aimer;1;passif;plus-que-parfait;2;amatus eras;tu avais été aimé;amo, as, are, aui, atum
amare;aimer;1;passif;plus-que-parfait;3;amatus erat;il avait été aimé;amo, as, are, aui, atum
amare;aimer;1;passif;plus-que-parfait;4;amati eramus;nous avions été aimé;amo, as, are, aui, atum
amare;aimer;1;passif;plus-que-parfait;5;amati eratis;vous aviez été aimé;amo, as, are, aui, atum
amare;aimer;1;passif;plus-que-parfait;6;amati erant;ils avaient été aimé;amo, as, are, aui, atum
"""


def get_verb_csv(pair):
    """
    Ask ChatGPT to generate the conjugated CSV for a latin/french verb pair (ex: amare / amo)

    *input* (one)
    pair (str): a latin/french verb pair (ex: "amare / amo")

    *output* (one)
    the generated CSV (with the column headers)
    """
    print(f"Get CSV for {pair}")

    # Use ChatCompletion with a short system message + user message
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": pair}
        ],
        temperature=0.0)

    verb_csv = response.choices[0].message.content.strip()
    return verb_csv


def get_pairs(verbs):
    """
    Get all the possible verb pairs (ex: amare / amo) from all the conjugated verbs loaded from the CSV file

    """
    pairs = set()
    for verb in verbs:
        pairs.add(verb["infinitive"] + " / " + verb["infinitif"])
    return pairs


def main():
    ###
    # Get verbs from the CSV file
    ###

    verbs = get_verbs("verbs_latin.csv")
    pairs = get_pairs(verbs)
    print(f"loaded {len(pairs)} verb pairs")

    ###
    # Get conjugations from ChatGPT and save to the new CSV file
    ###

    headers = "infinitive;infinitif;group;voice;tense;person;latin;french;primitive tenses\n"

    with open("new_verbs.csv", "w", encoding="utf-8-sig") as f:
        f.write(headers)
        for pair in sorted(pairs):
            start_time = time.time()

            # Ask ChatGPT to conjugate
            verb_csv = get_verb_csv(pair)

            # Remove the headers
            verb_csv = verb_csv.replace(headers, "")

            end_time = time.time()
            nlines = len(verb_csv.split('\n'))
            print(f"{nlines} conjugations generated in {end_time - start_time} seconds")

            # Write to the file
            f.write(verb_csv)
            f.write("\n")


if __name__ == "__main__":
    main()
