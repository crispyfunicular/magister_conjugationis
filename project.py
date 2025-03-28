import re
import sys
import csv
import random
import argparse
import emoji


def get_verbs(verbs_latin_csv):
    """ Loads all the verbs from a CSV file (format in README.md)

    *Input* (one)
    verbs_latin_csv = CSV filename

    *Output* (one)
    retlist_verbs = list of dicts (one per line)
    """

    list_verbs = []
    with open(verbs_latin_csv, encoding="utf-8-sig") as csvfile:
        csv.register_dialect('semicolumn', delimiter=';')
        reader = csv.DictReader(csvfile, dialect='semicolumn')
        for verb in reader:
            verb["latin"] = verb["latin"].replace("v", "u").replace("j", "i")
            verb["infinitive"] = verb["infinitive"].replace("v", "u").replace("j", "i")
            verb["primitive tenses"] = verb["primitive tenses"].replace("v", "u").replace("j", "i")
            verb["person"] = int(verb["person"])
            if verb["person"] not in range(0,7):
                raise ValueError(f"Invalid csv file, the person is invalid for {verb}")
            list_verbs.append(verb)
        return list_verbs


def get_tenses(list_verbs):
    """ Gets all the tenses available in the list of potential questions/answers (present, future,...) and lists them (only once each) in a dedicated list.

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


def get_groups(list_verbs):
    """ Gets all the verb groups available in the list of potential questions/answers (0, 1, 2, 3 or 4) and lists them (only once each) in a dedicated list.

    *Input* (one)
    list_verbs (list of dict) = the list of potential questions/answers

    *Output* (one)
    list_groups (list of str) = list of all the available groups (only one of each) in the csv.
        => Ex: ["0", "1", "3"]
    """

    list_groups = []
    for verb in list_verbs:
        if verb["group"] not in list_groups:
            list_groups.append(verb["group"])
    return list_groups


def filter_tense(tense_user, list_verbs):
    """ Filters the list of potential questions/answers (list_verbs) so as to keep only those matching the user's choice regarding the tense, if applicable.

    From main():
    parser.add_argument('-t', '--tense', type=str, choices=list_tenses, default=None, help="Choose a tense")
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


def filter_group(group_user, list_verbs):
    """ Filters the list of potential questions/answers (list_verbs) so as to keep only those matching the user's choice regarding the verb group, if applicable.

    From main():
    parser.add_argument('-g', '--group', type=str, choices=list_groups, default=None, help="Choose a verb group")
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


def filter_person(person_user, list_verbs):
    """ Filters the list of potential questions/answers (list_verbs) so as to keep only those matching the user's choice regarding the person, if applicable.

    From main():
    parser.add_argument('-p', '--person', type=int, choices=range(0,7), default=None, help="Choose a person")
    person_user = args.person

    *Input* (two)
    group_user (int) = the user's choice regarding the person (if applicable).
        => Ex: "4"
    list_verbs (list of dict) = the list of potential questions/answers

    *Output* (one)
    filtered_verbs (list of dict) = list of all the potential questions/answers, filtered according to the user's choice regarding the person.
        => Ex: a list with all the verbs, but only conjugated at the fourth person ("we").
    OR list_verbs (list of dict) = the output is the same as the input when the user has declared no choice regarding the verb group.
    """

    filtered_verbs = []
    if person_user:
        for verb in list_verbs:
            if person_user == verb["person"]:
                filtered_verbs.append(verb)
        return filtered_verbs
    else:
        return list_verbs


def get_difficulty(difficulty_user):
    """ Assigns the level of difficulty chosen by the user (if none, "easy" is the default level) to a number of possible attempts (int)
    #easy: 3 attempts for each verb (and 2 hints)
    #medium: 2 attempts for each verb (and only 1 hint)
    #hard: only 1 attemp for each verb (and no hint)

    From main():
    parser.add_argument('-d', '--difficulty', type=str, choices=["easy", "medium", "hard"], default="easy", help="Choose a difficulty level")
    max_attempts = get_difficulty(args.difficulty)

    *Input* (one)
    difficulty_user (str) = level of difficulty chosen by the user (if none, "easy" is the default level)

    *Output* (one)
    max_attempts (int) = number of possible attempts (how many answers the user can give before switching questions)
    """

    if difficulty_user == "easy":
        max_attempts = 3
    elif difficulty_user == "medium":
        max_attempts = 2
    elif difficulty_user == "hard":
        max_attempts = 1
    return max_attempts


def random_verb(list_verbs) -> dict:
    """ Randomly picks a line (dict) randomly from the list of all potential questions/answers (list of dict), which might have been previously filtered according to the user's choice, when applicable.

    From main():
    chosen_verb = random_verb(filtered_verbs)

    *Input* (one)
    list_verbs (list of dict): the list of potential questions/answers

    *Output* (one)
    a dict corresponding to a verb in latin, conjugated to one person and one tense, and its translation in French, as well as its Latin and French infinitive and primitive tenses
        => Ex: {amare;aimer;1;actif;imparfait;1;amabam;j'aimais;amo, as, are, avi, atum}
    """

    return random.choice(list_verbs)


def random_language(language_user):
    """ If the user has made no choice regarding the language (French or Latin) of the verb to translation, randomly assigns "French" or "Latin" to language_user.
    If the user has chosen either French or Latin, language_user remains unchanged

    From main():
    parser.add_argument('-l', '--language', type=str, choices=["latin", "french"], default=None, help="If you don't want to practice both languages, choose one of them")
    language_user = args.language
    language_question = random_language(language_user)

    *Input* (one)
    language_user (str/None): either "latin"/"french" if the user has chosen so or None if the user has made no choice regarding the language

    *Output* (one)
    language_user (str): either the user's choice (if applicable) or the random choice of the function (if language_user == None)
        => "latin" or "french"
    """

    if not language_user:
        return random.choice(["latin", "french"])
    return language_user


def get_language_answer(language_question):
    """ Determines the language of the answer according to the language question (such as decided by the user or randomly picked by the program)
    *Input* (one)
    language_question (str) = the language ("french" or "latin") chosen by the user (if applicable) or randomly picked by random_language(), in which the language is asked.

    *Output* (one)
    language_answer (str) = the language of the answer expected from the user

        - if language_question == "latin" -> language_answer == "french" (output)
            => Ex: The asked verb will be "amo" and the expected answer will be "j'aime"
        - if language_question == "french" -> language_answer == "latin" (output)
            => Ex: The asked verb will be "j'aime" and the expected answer will be "amo"
    """

    if language_question == "latin":
        language_answer = "french"
    elif language_question == "french":
        language_answer = "latin"
    else:
        raise ValueError
    return language_answer


def choose_question(latin: str, french: str, language_question: str) -> (str, str, str):
    """ Determines the verb to be displayed (asked to the user) and the language of the question (Latin or French) to which it must be translated according to the user's previous choice.

    *Input* (three)
    latin (str) = the verb in Latin for a given dict. Ex: "amo"
    french (str) = the verb in French for the same given dict. Ex: "j'aime"
    language_question = the language ("french" or "latin") chosen by the user (if applicable) or randomly picked by random_language(), in which the language is asked (str).
        - if language_question == "latin" -> the asked verb will be "amo"
        - if language_question == "french" -> the asked verb will be "j'aime"

    *Output* (three)
    question (str) = the verb that will be asked to the user.
        => Ex: If language_question = "latin", the verb used for the question will be the verb in Latin.
    correct_answer (str) = the verb that has not been picked for the question and that will be used later to check the user's answer.
        => Ex: If language_question = "latin", the verb used for the answer will be the verb in French.
    translation (str) = the language of the answer according to the language of the question. Will be used only in the question displayed to the user.
        => Ex: If language_question = "latin", translation = "French"
    """

    if language_question == "latin":
        question = latin
        correct_answer = french
        translation = "French"
    elif language_question == "french":
        question = french
        correct_answer = latin
        translation = "Latin"
    return question, correct_answer, translation


def get_all_answers(list_verbs, question, language_question, language_answer):
    """ Gets all the correct answers for one question. Some verbs have more than one correct translation and any of them must be accepted.
        => Ex: "lego" -> ["je lis", "je cueille", "je choisis"]
        => Ex: "je pense" -> ["puto", "cogito"]

    *Input* (three)
    list_verbs (list of dict) = the list of potential questions/answers
    question (str) = the verb that will be asked to the user.
        => Ex: If language_question = "latin", the verb used for the question will be the verb in Latin.
    language_question (str) = the language ("french" or "latin") chosen by the user (if applicable) or randomly picked by random_language(), in which the language is asked.
        - if language_question == "latin" -> the asked verb will be "amo"
        - if language_question == "french" -> the asked verb will be "j'aime"

    *Output* (one)
    list_all_answers (list of dict) = list of all the possible answers
    """

    list_all_answers = []
    for verb in list_verbs:
        if question == verb[language_question]:
            list_all_answers.append(verb[language_answer])
    return list_all_answers


def get_hint(chosen_verb, language_question, attempts):
    """ Gives a hint according to the language of the question (Latin or French) and the number of attempts.
    * First attempt: no hint
    * Second attempt:
        - if the question is in French (language_question = "french"): infinitive (ex: "amare")
        - if the question is in Latin (language_question = "latin"): nothing (None)
    * Third (and last) attempt (depending on the difficulty level):
        - if the question is in French (language_question = "french"): primitive tenses (ex: "amo, as, are, aui, atum")
        - if the question is in Latin (language_question = "latin"): French infinitive ("infinitif") (ex: "aimer")

    *Input* (three)
    chosen_verb = dict
    language_question = the language ("french" or "latin") chosen by the user (if applicable) or randomly picked by random_language(), in which the language is asked (str).
        - if language_question == "latin" -> the asked verb will be "amo"
        - if language_question == "french" -> the asked verb will be "j'aime"
    attempts = 1, 2 or 3 (depending on the difficulty level) (int)

    *Output* (one)
    hint = None, infinitive, primitive tense or French infinitif, depending on the settings (None or str)
    """

    if language_question == "french":
        if attempts == 1:
            return chosen_verb["infinitive"]
        elif attempts == 2:
            return chosen_verb["primitive tenses"]
    if language_question == "latin":
        if attempts == 2:
            return chosen_verb["infinitif"]


def ask_verb(question, translation, hint) -> str:
    """
    Displays a verb in Latin or in French and asks the user to write the answer in input.
    Checks the answer's format. If not valid, the user must try again

    *Input* (none)
    Will get the user's answer in input() (str)

    *Output* (one)
    user_answer (str): the user's answer, as asked in input()
    """

    while True:
        print((f'Which is the {translation} translation of "{question}"?'))
        if hint:
            print("Here is a hint:", hint)
        user_answer = input("Answer: ").strip()
        matches = re.search(r"^[a-z ']+", user_answer, re.IGNORECASE)
        if matches:
            return user_answer
        else:
            print("Invalid format, try again")


def compare_answers(user_answer, list_all_answers, language_answer):
    """ Compares the answers given by the user with the correct answer from the CSV file. If they matches, returns True. If they don't, returns False.

    *Input* (three)
    user_answer (str) = the answer given by the user
        => Ex: "je cueille"
    list_all_answers (list of dict) = list of all the possible answers
        => Ex: ["je lis", "je cueille", "je choisis"]
    language_answer (str) = the language of the answer expected from the user
        => Ex: "french"

    *Output* (one)
    True (Boolean) = if the user's answer is the same than the correct answer from the CSV file (or one of the possible correct answers)
    OR False (Boolean) = if the two answers don't match
    """

    #list_all_answers = [correct_answer.lower().replace("v", "u") for correct_answer in list_all_answers if the language of the answer is Latin]
    user_answer = user_answer.lower()
    if language_answer == "latin":
        user_answer = user_answer.replace("v", "u").replace("j", "i")
    #In case the user types "elle(s)" for "il(s)"
    user_answer = re.sub(r"^elle(s?) (.*)$", r"il\1 \2", user_answer)

    for correct_answer in list_all_answers:
        if user_answer == correct_answer:
            return True
    return False


def main():
    """
    #1 get_verbs(): Loads all the verbs from a CSV file (format in README.md)
    #2(a) get_tenses(): Gets all the tenses available in the list of potential questions/answers (present, future,...) and lists them (only once each) in a dedicated list.
    #2(b) get_groups(): Gets all the verb groups available in the list of potential questions/answers (0, 1, 2, 3 or 4) and lists them (only once each) in a dedicated list.
    #2(c): We assume that all the persons (I, you, he...) are in the list of potential questions/answers so we don't list them
    #3 filter_tense() filter_group() filter_person(): Filters the list of potential questions/answers (list_verbs) so as to keep only those matching the user's choice regarding the tense / verb group / person, if applicable.
    #4 get_difficulty(): Assigns the level of difficulty chosen by the user (if none, "easy" is the default level) to a number of possible attempts (int)
    #5 random_verb(): Randomly picks a line (dict) randomly from the list of all potential questions/answers (list of dict), which might have been previously filtered according to the user's choice, when applicable.
    #6 random_language(): If the user has made no choice regarding the language (French or Latin) of the verb to translation, randomly assigns "French" or "Latin" to language_user. If the user has chosen either French or Latin, language_user remains unchanged
    #7 get_language_answer(): Determines the language of the answer according to the language question (such as decided by the user or randomly picked by the program)
    #8 choose_question(): Determines the verb to be displayed (asked to the user) and the language of the question (Latin or French) to which it must be translated according to the user's previous choice.
    #9 get_all_answers(): Gets all the correct answers for one question. Some verbs have more than one correct translation and any of them must be accepted.
    #10 get_hint(): Gives a hint according to the language of the question (Latin or French) and the number of attempts.
    #11 ask_verb(): Displays a verb in Latin or in French and asks the user to write the answer in input. Checks the answer's format. If not valid, the user must try again
    #12 compare_answers(): Compares the answers given by the user with the correct answer from the CSV file. If they matches, returns True. If they don't, returns False.
    """

    ###
    # Load CSV file
    ###

    verbs_latin_csv = "verbs_latin.csv"
    try:
        list_verbs = get_verbs(verbs_latin_csv)
    except FileNotFoundError:
        print("File not found")
        sys.exit(1)
    list_tenses = get_tenses(list_verbs)
    list_groups = get_groups(list_verbs)

    ###
    # Get CLI params
    ###

    parser = argparse.ArgumentParser(
                    prog='project.py',
                    description='Asks the user the translation of a conjugated verb in Latin or in French',
                    epilog='Bonam fortunam!')
    parser.add_argument('-c', '--count', type=int, default=5, help="Number of verbs to practice")
    parser.add_argument('-d', '--difficulty', type=str, choices=["easy", "medium", "hard"], default="easy", help="The difficulty level which determines the number of possible attempts (3, 2 or 1)")
    parser.add_argument('-g', '--group', type=str, choices=list_groups, default=None, help="The verb group (ex: 1) to practice (0 corresponds to \"sum\" and its derivatives)")
    parser.add_argument('-l', '--language', type=str, choices=["latin", "french"], default=None, help="The language (Latin and/or French) from which the user wants to translate. If they don't want to practice both languages, they can choose one of them")
    parser.add_argument('-p', '--person', type=int, choices=range(0,7), default=None, help="The person (1 to 6) to practice")
    parser.add_argument('-t', '--tense', type=str, choices=list_tenses, default=None, help="The tense (ex: \"présent\") to practice")
    parser.add_argument('--debug', action='store_true', help="Enable debug mode")
    args = parser.parse_args()
    number_verbs = args.count

    language_user = args.language
    max_attempts = get_difficulty(args.difficulty)
    tense_user = args.tense
    group_user = args.group
    person_user = args.person
    debug = args.debug

    ###
    # Filter verbs according to params
    ###

    if debug:
        print(f"Loaded {len(list_verbs)} from {verbs_latin_csv}")

    filtered_verbs = filter_tense(tense_user, list_verbs)
    filtered_verbs = filter_group(group_user, filtered_verbs)
    filtered_verbs = filter_person(person_user, filtered_verbs)
    if len(filtered_verbs) == 0:
        print("No available verbs for these choices")
        sys.exit(1)

    if debug:
        print(f"Kept {len(filtered_verbs)} after filtering by tense and group")

    correct_answers = []
    wrong_answers = []
    #How many verbs the user has already seen
    total_count = 0
    while total_count < number_verbs:
        chosen_verb = random_verb(filtered_verbs)
        french = chosen_verb["french"]
        latin = chosen_verb["latin"]
        language_question = random_language(language_user)
        language_answer = get_language_answer(language_question)
        question, correct_answer, translation = choose_question(latin, french, language_question)
        list_all_answers = get_all_answers(list_verbs, question, language_question, language_answer)
        if debug:
            print(list_all_answers)


        total_count += 1

        #How many tries for the asked verb
        attempts = 0
        remaining_attempts = max_attempts
        print(f"Question number {total_count}/{number_verbs}")
        while remaining_attempts:
            hint = get_hint(chosen_verb, language_question, attempts)
            #Question
            user_answer = ask_verb(question, translation, hint)
            attempts += 1
            remaining_attempts -= 1

            if compare_answers(user_answer, list_all_answers, language_answer):
                displayed_answers = ", ".join(list_all_answers)
                correct_answers.append(f"{question} = {displayed_answers}")
                print(emoji.emojize("Bene factum! :party_popper:"))
                break

            if remaining_attempts:
                s = "s" if remaining_attempts > 1 else ""
                print(emoji.emojize(f"Errare humanum est... :person_shrugging: try {remaining_attempts} more time{s}"))
                print()
            else:
                displayed_answers = ", ".join(list_all_answers)
                wrong_answers.append(f'{question} = {displayed_answers} (not "{user_answer}")')
                print(f'The correct answer was "{correct_answer}"')

        #Doesn't print the message when there is no other verb coming (i.e the limit has been reached)
        if total_count < number_verbs:
            print()
            print("Let's try another verb!")

    print()
    print("***********************")
    if len(correct_answers) > 0:
        s = "s" if len(correct_answers) > 1 else ""
        was_were = "were" if len(correct_answers) > 1 else "was"
        print(emoji.emojize(f":check_mark_button: The correct answer{s} {was_were}:"))
        for answer in correct_answers:
            print("*", answer)
    if len(wrong_answers) > 0:
        s = "s" if len(wrong_answers) > 1 else ""
        was_were = "were" if len(wrong_answers) > 1 else "was"
        print()
        print(emoji.emojize(f":cross_mark: The incorrect answer{s} {was_were}:"))
        for answer in wrong_answers:
            print("*", answer)


if __name__ == "__main__":
    main()
