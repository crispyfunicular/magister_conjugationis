import json
import sys
import random
import argparse

debug = False


def get_verbs(json_path: str) -> list[dict]:
    """Loads all the verbs from a .json file

    *Input* (one)
    verbs_path = path to a json file (str)

    *Output* (one)
    verbs = list of dicts (one per inflected form)
    """
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_tenses(list_verbs) -> list[str]:
    """Gets all the tenses available in the list of potential questions/answers (present, future,...) and lists them (only once each) in a dedicated list.

    *Input* (one)
    list_verbs (list of dict) = the list of potential questions/answers

    *Output* (one)
    list_tenses (list of str) = list of all the available tenses (names in French, and only one of each) in the csv.
        => Ex: ["present", "imparfait", "futur"]
    """

    list_tenses = []
    for verb in list_verbs:
        if verb["tense"] not in list_tenses:
            list_tenses.append(verb["tense"])
    return list_tenses


def get_groups(list_verbs) -> list[int]:
    """Gets all the verb groups available in the list of potential questions/answers (0, 1, 2, 3 or 4) and lists them (only once each) in a dedicated list.

    *Input* (one)
    list_verbs (list of dict) = the list of potential questions/answers

    *Output* (one)
    list_groups (list of int) = list of all the available groups (only one of each) in the csv.
        => Ex: [0, 1, 3]
    """

    list_groups = []
    for verb in list_verbs:
        if verb["group"] not in list_groups:
            list_groups.append(verb["group"])
    list_groups.sort()

    return list_groups


def filter_tense(tense_user, list_verbs) -> list[dict]:
    """Filters the list of potential questions/answers (list_verbs) so as to keep only those matching the user's choice regarding the tense, if applicable.

    From main():
    parser.add_argument('-t', '--temps', type=str, choices=list_tenses, default=None, help="Le temps (ex: "présent") que vous souhaitez pratiquer")
    tense_user = args.tense

    *Input* (two)
    tense_user (str) = the user's choice regarding the tense (if applicable).
        => Ex: "present"
    list_verbs (list of dict) = the list of potential questions/answers

    *Output* (one)
    filtered_verbs (list of dict) = list of all the potential questions/answers, filtered according to the user's choice regarding the tense.
        => Ex: a list with only the verbs in present.
    OR list_verbs (list of dict) = the output is the same as the input when the user has declared no choice regarding the tense.
    """

    filtered_verbs = []
    if tense_user:
        for verb in list_verbs:
            if tense_user == verb["tense"]:
                filtered_verbs.append(verb)
        return filtered_verbs
    else:
        return list_verbs


def filter_group(group_user, list_verbs) -> list[dict]:
    """Filters the list of potential questions/answers (list_verbs) so as to keep only those matching the user's choice regarding the verb group, if applicable.

    From main():
    parser.add_argument('-g', '--groupe', type=str, choices=list_groups, default=None, help="Le groupe verbal (ex: 1) que vous souhaitez réviser (0 correspond à "sum" et ses dérivés)")
    group_user = args.group

    *Input* (two)
    group_user (int) = the user's choice regarding the verb group (if applicable).
        => Ex: "2"
    list_verbs (list of dict) = the list of potential questions/answers

    *Output* (one)
    filtered_verbs (list of dict) = list of all the potential questions/answers, filtered according to the user's choice regarding the verb group.
        => Ex: a list with only the verbs of the second group.
    OR list_verbs (list of dict) = the output is the same as the input when the user has declared no choice regarding the verb group.
    """

    filtered_verbs = []
    if group_user:
        for verb in list_verbs:
            if group_user == verb["group"]:
                filtered_verbs.append(verb)
        return filtered_verbs
    else:
        return list_verbs


def filter_person(person_user, list_verbs) -> list[dict]:
    """Filters the list of potential questions/answers (list_verbs) so as to keep only those matching the user's choice regarding the person, if applicable.

    From main():
    parser.add_argument('-p', '--personne', type=int, choices=range(0,7), default=None, help="La personne (comprise entre 1 et 6) que vous souhaitez pratiquer")
    person_user = args.person

    *Input* (two)
    person_user (int) = the user's choice regarding the person (if applicable).
        => Ex: "4"
    list_verbs (list of dict) = the list of potential questions/answers

    *Output* (one)
    filtered_verbs (list of dict) = list of all the potential questions/answers, filtered according to the user's choice regarding the person.
        => Ex: a list with all the verbs, but only conjugated at the fourth person ("we").
    OR list_verbs (list of dict) = the output is the same as the input when the user has declared no choice regarding the person.
    """

    filtered_verbs = []
    if person_user:
        for verb in list_verbs:
            if person_user == verb["person"]:
                filtered_verbs.append(verb)
        return filtered_verbs
    else:
        return list_verbs


def filter_voice(voice_user, list_verbs) -> list[dict]:
    """Filters the list of potential questions/answers (list_verbs) so as to keep only those matching the user's choice regarding the voice, if applicable.

    From main():
    parser.add_argument('-v', '--voix', type=str, choices=["actif", "passif"], default=None, help="La voix (actif ou passif) que vous souhaitez pratiquer")
    voice_user = args.voice

    *Input* (two)
    voice_user (str) = the user's choice regarding the voice (if applicable).
        => Ex: "active"
    list_verbs (list of dict) = the list of potential questions/answers

    *Output* (one)
    filtered_verbs (list of dict) = list of all the potential questions/answers, filtered according to the user's choice regarding the voice.
        => Ex: a list with all the verbs, but only conjugated at the passive voice.
    OR list_verbs (list of dict) = the output is the same as the input when the user has declared no choice regarding the voice.
    """

    filtered_verbs = []
    if voice_user:
        for verb in list_verbs:
            if voice_user == verb["voice"]:
                filtered_verbs.append(verb)
        return filtered_verbs
    else:
        return list_verbs


def filter_mood(mood_user, list_verbs) -> list[dict]:
    """Filters the list of potential questions/answers (list_verbs) so as to keep only those matching the user's choice regarding the mood, if applicable.

    From main():
    parser.add_argument('-m', '--mode', type=str, choices=["indicatif", "subjonctif"], default=None, help="Le mode (indicatif ou subjonctif) que vous souhaitez pratiquer")
    mood_user = args.mood

    *Input* (two)
    mood_user (str) = the user's choice regarding the mood (if applicable).
        => Ex: "active"
    list_verbs (list of dict) = the list of potential questions/answers

    *Output* (one)
    filtered_verbs (list of dict) = list of all the potential questions/answers, filtered according to the user's choice regarding the mood.
        => Ex: a list with all the verbs, but only conjugated at the subjonctive mood.
    OR list_verbs (list of dict) = the output is the same as the input when the user has declared no choice regarding the mood.
    """
    filtered_verbs = []
    if mood_user:
        for verb in list_verbs:
            if mood_user == verb["mood"]:
                filtered_verbs.append(verb)
        return filtered_verbs
    else:
        return list_verbs


def random_verb(list_verbs: list[dict]) -> dict:
    """Randomly picks a line (dict) randomly from the list of all potential questions/answers (list of dict), which might have been previously filtered according to the user's choice, when applicable.

    From main():
    chosen_verb = random_verb(filtered_verbs)

    *Input* (one)
    list_verbs (list of dict): the list of potential questions/answers

    *Output* (one)
    a dict corresponding to a verb in latin, conjugated to one person and one tense, and its translation in French, as well as its Latin and French infinitive and primitive tenses
        => Ex: {amare;aimer;1;actif;imparfait;1;amabam;j'aimais;amo, as, are, avi, atum}
    """

    return random.choice(list_verbs)


def ask(message: str, validator, error_message):
    while True:
        try:
            result = input(message).strip()
            if validator(result):
                return result
            else:
                print(error_message)
        except Exception as e:
            print(e)
            print(error_message)


def ask_verb(verb) -> int:
    score = 0

    print("Nouveau verbe à trouver :", verb["latin"])

    # Personne (1 à 6)
    person = verb["person"]

    while True:
        if debug:
            print(person)
        person_input = int(
            ask(
                "Indiquer la personne (de 1 à 6) : ",
                lambda x: int(x) in range(1, 7),
                "La personne doit être comprise entre 1 et 6.",
            )
        )
        if person == person_input:
            score += 1
            print("Bravo !")
            break
        else:
            print("Mauvaise réponse ! Errare humanum est...")
            choice_user = int(
                ask(
                    "Essayer à nouveau cette question (1), voir les temps primitifs (2) ou voir la réponse (3) ? ",
                    lambda x: int(x) in range(1, 4),
                    "La réponse doit être comprise entre 1 et 3.",
                )
            )
            if choice_user == 1:
                continue
            elif choice_user == 2:
                print("Voici les temps primitifs :", verb["primitive tenses"])
            elif choice_user == 3:
                print(person)
                break

    # Temps (présent, imparfait, futur, parfait, plus-que-parfait ou futur antérieur)
    tense = verb["tense"]

    while True:
        if debug:
            print(tense)
        print(
            "Temps possibles : présent, imparfait, futur, parfait, plus-que-parfait ou futur antérieur"
        )
        tense_input = input("Réponse : ").strip().lower()
        if tense == tense_input:
            score += 1
            print("Bravo !")
            break
        else:
            print("Mauvaise réponse ! Errare humanum est...")
            choice_user = int(
                ask(
                    "Essayer à nouveau cette question (1), voir les temps primitifs (2) ou voir la réponse (3) ? ",
                    lambda x: int(x) in range(1, 4),
                    "La réponse doit être comprise entre 1 et 3.",
                )
            )
            if choice_user == 1:
                continue
            elif choice_user == 2:
                print("Voici les temps primitifs :", verb["primitive tenses"])
            elif choice_user == 3:
                print(tense)
                break

    # Voix (passif ou actif)
    voice = verb["voice"]

    while True:
        if debug:
            print(voice)
        voice_input = ask(
            "Indiquer la voix (actif ou passif) : ",
            lambda x: x.lower() in ["actif", "passif"],
            "La réponse doit être soit 'actif', soit 'passif'.",
        )

        if voice == voice_input:
            score += 1
            print("Bravo !")
            break
        else:
            print("Mauvaise réponse ! Errare humanum est...")
            choice_user = int(
                ask(
                    "Essayer à nouveau cette question (1), voir les temps primitifs (2) ou voir la réponse (3) ? ",
                    lambda x: int(x) in range(1, 4),
                    "La réponse doit être comprise entre 1 et 3.",
                )
            )
            if choice_user == 1:
                continue
            elif choice_user == 2:
                print("Voici les temps primitifs :", verb["primitive tenses"])
            elif choice_user == 3:
                print(voice)
                break

    # Mode (indicatif ou subjonctif)
    mood = verb["mood"]

    while True:
        if debug:
            print(mood)
        mood_input = (
            input("Indiquer le mode (indicatif ou subjonctif) : ").strip().lower()
        )
        if mood == mood_input:
            score += 1
            print("Bravo !")
            break
        else:
            print("Mauvaise réponse ! Errare humanum est...")
            choice_user = int(
                ask(
                    "Essayer à nouveau cette question (1), voir les temps primitifs (2) ou voir la réponse (3) ? ",
                    lambda x: int(x) in range(1, 4),
                    "La réponse doit être comprise entre 1 et 3.",
                )
            )
            if choice_user == 1:
                continue
            elif choice_user == 2:
                print("Voici les temps primitifs :", verb["primitive tenses"])
            elif choice_user == 3:
                print(mood)
                break

    # Traduction
    translations = verb["translation"]

    while True:
        if debug:
            print(translations)
        translation_input = (
            input("Indiquer la traduction en français (à l'infinitif) : ")
            .strip()
            .lower()
        )
        if translation_input in translations:
            score += 1
            print("Bravo !")
            break
        else:
            print("Mauvaise réponse ! Errare humanum est...")
            choice_user = int(
                ask(
                    "Essayer à nouveau cette question (1) ou voir la réponse (2) ? ",
                    lambda x: int(x) in range(1, 3),
                    "La réponse doit être comprise entre 1 et 2.",
                )
            )
            if choice_user == 1:
                continue
            elif choice_user == 2:
                print(", ".join(translations))
                break

    return score


def ask_verbs(verbs: list[dict], direction):
    rounds_input = int(
        ask(
            "Combien de verbes voulez-vous pratiquer (entre 1 et 10) ? ",
            lambda x: int(x) in range(1, 11),
            "Entrez un nombre compris entre 1 et 10",
        )
    )
    total_score = 0

    for _ in range(rounds_input):
        verb = random_verb(verbs)

        if not direction:
            choice = random.choice(["latin", "français"])
        else:
            choice = direction

        if choice == "latin":
            score = ask_verb(verb) / 5
        elif choice == "français":
            score = ask_verb_reverse(verb)

        total_score += score
    print(f"Score total : {total_score}/{rounds_input}")
    print("Prêt-e pour une nouvelle partie ?")


def personne(person: int) -> str:
    nb = "singulier"

    if person > 3:
        person -= 3
        nb = "pluriel"

    return f"{person}e personne du {nb}"


def ask_verb_reverse(verb) -> int:
    latin = verb["latin"]
    score = 0

    while True:
        if debug:
            print(latin)

        answer = ask(
            f"Indiquer la forme fléchie pour le(s) verbe(s) '{", ".join(verb["translation"])}', à la {personne(verb["person"])}, {verb["tense"]}, {verb["voice"]}, {verb["mood"]} : ",
            lambda x: x,
            "Veuillez indiquer une réponse.",
        )
        if answer == latin:
            score += 1
            print("Bravo !")
            break
        else:
            print("Mauvaise réponse ! Errare humanum est...")
            choice_user = int(
                ask(
                    "Essayer à nouveau cette question (1), voir les temps primitifs (2), voir le lemme (3) ou voir la réponse (4) ? ",
                    lambda x: int(x) in range(1, 5),
                    "La réponse doit être comprise entre 1 et 4.",
                )
            )
            if choice_user == 1:
                continue
            if choice_user == 2:
                print("Voici les temps primitifs :", verb["primitive tenses"])
            if choice_user == 3:
                print("Voici le lemme :", verb["lemma"])
            if choice_user == 4:
                print(latin)
                break

    return score


def main():
    """
    #1 get_verbs(): Loads all the verbs from a CSV file (format in README.md)
    #2(a) get_tenses(): Gets all the tenses available in the list of potential questions/answers (present, future,...) and lists them (only once each) in a dedicated list.
    #2(b) get_groups(): Gets all the verb groups available in the list of potential questions/answers (0, 1, 2, 3 or 4) and lists them (only once each) in a dedicated list.
    #2(c): We assume that all the persons (I, you, he...) are in the list of potential questions/answers so we don't list them
    #3 filter_tense() filter_group() filter_person(): Filters the list of potential questions/answers (list_verbs) so as to keep only those matching the user's choice regarding the tense / verb group / person, if applicable.
    #4 random_verb(): Randomly picks a line (dict) randomly from the list of all potential questions/answers (list of dict), which might have been previously filtered according to the user's choice, when applicable.
    #5 ask_verbs(): Displays a verb in Latin or in French and asks the user to write the answer in input. Checks the answer's format. If not valid, the user must try again
    """

    ###
    # Load JSON files from a folder
    ###

    verbs_latin_path = "verbs_latin.json"
    list_verbs = get_verbs(verbs_latin_path)
    list_tenses = get_tenses(list_verbs)
    list_groups = get_groups(list_verbs)

    ###
    # Get CLI params
    ###

    parser = argparse.ArgumentParser(
        prog="project.py",
        description="Interroge l'utilisateur sur les verbes latins",
        epilog="Bonam fortunam!",
    )
    parser.add_argument(
        "-d",
        "--direction",
        type=str,
        choices=["latin", "français"],
        default=None,
        help="latin : latin -> français ; français : français -> latin",
    )
    parser.add_argument(
        "-g",
        "--groupe",
        type=int,
        choices=list_groups,
        default=None,
        help='Le groupe verbal (ex: 1) que vous souhaitez réviser (0 correspond à "sum" et ses dérivés)',
    )
    parser.add_argument(
        "-p",
        "--personne",
        type=int,
        choices=range(0, 7),
        default=None,
        help="La personne (comprise entre 1 et 6) que vous souhaitez pratiquer",
    )
    parser.add_argument(
        "-t",
        "--temps",
        type=str,
        choices=list_tenses,
        default=None,
        help='Le temps (ex: "présent") que vous souhaitez pratiquer',
    )
    parser.add_argument(
        "-v",
        "--voix",
        type=str,
        choices=["actif", "passif"],
        default=None,
        help="La voix (actif ou passif) que vous souhaitez pratiquer",
    )
    parser.add_argument(
        "-m",
        "--mode",
        type=str,
        choices=["indicatif", "subjonctif"],
        default=None,
        help="Le mode (indicatif ou subjonctif) que vous souhaitez pratiquer",
    )
    parser.add_argument("--debug", action="store_true", help="activer le mode debug")
    args = parser.parse_args()

    direction_user = args.direction
    tense_user = args.temps
    group_user = args.groupe
    person_user = args.personne
    voice_user = args.voix
    mood_user = args.mode

    global debug
    debug = args.debug

    ###
    # Filter verbs according to params
    ###

    if debug:
        print(f"Loaded {len(list_verbs)} from {verbs_latin_path}")

    filtered_verbs = filter_tense(tense_user, list_verbs)
    filtered_verbs = filter_group(group_user, filtered_verbs)
    filtered_verbs = filter_person(person_user, filtered_verbs)
    filtered_verbs = filter_voice(voice_user, filtered_verbs)
    filtered_verbs = filter_mood(mood_user, filtered_verbs)
    if len(filtered_verbs) == 0:
        print("No available verbs for these choices")
        sys.exit(1)

    if debug:
        print(f"Kept {len(filtered_verbs)} after filtering")

    ask_verbs(filtered_verbs, direction_user)


if __name__ == "__main__":
    main()
