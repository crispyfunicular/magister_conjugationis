# MAGISTER CONJUGATIONIS
A Python program developped by Morgane Bona-Pellissier, 2025

CS50's Introduction to Pogramming with Python

## YouTube video demo
Link: https://youtu.be/U4--fNsrio4

## Description
This program asks the user to translate to French a conjugated verb in Latin, or the other way around (from Latin to French). If the user fails, they can try 1 or 2 more times (depending on the difficulty level) and get a **hint**, according to the following pattern:
* First attempt -> no hint
* Second attempt:
    - if the question is in French (language_question = "french") -> infinitive (ex: "amare")
    - if the question is in Latin (language_question = "latin") -> nothing (None)
* Third (and last) attempt (depending on the difficulty level):
    - if the question is in French (language_question = "french") -> primitive tenses (ex: "amo, as, are, aui, atum")
    - if the question is in Latin (language_question = "latin") -> French infinitive ("infinitif") (ex: "aimer")

When typing the command line, the user can choose a **difficulty level**:
* easy (by default): 3 attempts for each verb (and 2 hints)
* medium: 2 attempts for each verb (and only 1 hint)
* hard: only 1 attemp for each verb (and no hint)


## Some fundamental notions regarding the Latin conjugations
Latin verbs are usually designated by their so called "primitive tenses" (ex: "amo, as, are, avi, atum"), which carry a lot of information, such as the **group** the verb belongs to.
Verbs are ordered in 4 (sometimes 5) groups:
- (1) "o, as, are"
- (2) "eo, es, ere"
- (3) "o, is, ere"
- (4) "io, is, ere"
- (5) "io, is ire"

The letters "u" and "v", in the one hand, and "i" and "j", in the other hand, are interchangeable. Consequently, "amavi" is as valid as "amaui", and "jussi" is as valid as "iussi".

The verbal forms bear no gender distinction. Consequently, "amat" can be translated to "he loves" as well to "she loves".

There is a many-to-many relationship between the French and Latin verbs, which means that one Latin verb (ex: "lego") can have multiple correct answers in French (ex: "je lis", "je cueille", "je choisis"), and conversely one French verb (ex: "je pense") can have multiple correct answers in Latin (ex: "puto", "cogito"). Therefore, we told the programm to accept any possible answers and not only the one corresponsing to the specific pair picked for the question.

## How we selected and listed our verbs in the CSV file
We based our the list of verbs and tenses on the one issued by the [Paris Nanterre University's DUCLA degree](https://dep-lettresclassiques.parisnanterre.fr/latin-et-grec-pour-tous). We created a Excel sheet were we entered the following colomns:
- (A) "infinitive" : the infinitive in Latin (-> "amare")
- (B) "infinitif": the infinitive in French (-> "aimer")
- (C) "group": the group (1 to 4) the Latin verb in column (G) belongs to (-> 1)
- (D) "voice": the voice (active or passive) in which the Latin verb in column (G) is conjugated to (-> "active")
- (E) "tense": the tense in which the Latin verb in column (G) is conjugated to (-> "present")
- (F) "person": the person (1st to 6th) in which the Latin verb in column (G) is conjugated to (-> "1")
- (G) "latin": the Latin verb conjugated to one person, one tense and one voice (-> "amo")
- (H) "french": the French translation of the Latin verb in column (G) (-> "j'aime")
- (I) "primitive tenses": the primitive tenses related to the Latin verb in column (G) (->"amo, as, are, avi, atum")

So as not to type manually each of the lines, we created a dedicated ChatGPT chat ([Magister Conjugationis](https://chatgpt.com/g/g-67cdb50a34d88191b89a51e319d99ccb-magister-conjugationis/c/67ce0079-a49c-800a-bf79-7790aaff6157)) where we explained our constraints to ChatGPT and gave it the format (corresponding to the A to I Excel columns) we wished to get its answers in. We then gave it one by one all the verbs that we wanted it to conjugate for us.

We chose to work on an Excell sheet because it was very handy. We were indeed able to easily import all the ChatGPT answers, modify them if needed, and export the Excel sheet to a CSV format readable by the Python program. When exporting our data to a CSV file, we had to chose the "UTF-8" option because of the French accents (ex: "j'ai aimé") and the "semicolon delimiter" option instead of the regular "comma delimiter" option because of the Latin primitive tenses, which contain commas (ex: "amo, as, are, avi, atum").

## How to set up the environment
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## How to use the program

```
project/ $ python project.py -h
usage: project.py [-h] [-c COUNT] [-l {latin,french}] [-d {easy,medium,hard}] [-t {present,futur,imparfait,parfait,futur antérieur,plus-que-parfait,présent}] [-g {1,2,3,4,0}] [-p {0,1,2,3,4,5,6}] [--debug]

Asks the user the translation of a conjugated verb in Latin or in French

options:
  -h, --help            show this help message and exit
  -c COUNT, --count COUNT
                        Number of verbs to practice
  -l {latin,french}, --language {latin,french}
                        The language (Latin and/or French) from which the user wants to translate. If they don't want to practice both languages, they can choose one of them
  -d {easy,medium,hard}, --difficulty {easy,medium,hard}
                        The difficulty level which determines the number of possible attempts (3, 2 or 1)
  -t {présent,futur,imparfait,parfait,futur antérieur,plus-que-parfait}, --tense {présent,futur,imparfait,parfait,futur antérieur,plus-que-parfait}
                        The tense (ex: "présent") to practice
  -g {1,2,3,4,0}, --group {1,2,3,4,0}
                        The verb group (ex: 1) to practice (0 corresponds to "sum" and its derivatives)
  -p {0,1,2,3,4,5,6}, --person {0,1,2,3,4,5,6}
                        The person (1 to 6) to practice
  --debug               Enable debug mode

Bonam fortunam!
```

```
project/ $ python project.py -c 2
Question number 1/2
Which is the Latin translation of "vous disiez"?
Answer: dicebatis
Bene factum! 🎉

Let's try another verb!
Question number 2/2
Which is the Latin translation of "vous combattez"?
Answer: pugnattis
Errare humanum est... 🤷 try 2 more time

Which is the Latin translation of "vous combattez"?
Here is a hint: pugnare
Answer: pugnattis
Errare humanum est... 🤷 try 1 more time

Which is the Latin translation of "vous combattez"?
Here is a hint: pugno, as, are, aui, atum
Answer: pugnattis
The correct answer was "pugnatis"

***********************
✅ The correct answers were:
* vous disiez = dicebatis

❌ The incorrect answers were:
* vous combattez = pugnatis (not "pugnattis")
```

