import pytest
from project import *

def get_test_verbs():
    return get_verbs("verbs_latin_test.csv")



def test_get_difficulty():
    assert get_difficulty("easy") == 3
    assert get_difficulty("medium") == 2
    assert get_difficulty("hard") == 1


def test_get_verbs():
    verbs = get_test_verbs()
    assert len(verbs) > 0
    assert verbs[0]["person"] == 1
    assert verbs[0]["primitive tenses"] == "amo, as, are, aui, atum"
    assert verbs[1]["latin"] == "iubebo"
    assert verbs[1]["french"] == "j'ordonnerai"
    assert verbs[1]["infinitive"] == "iubere"


def test_get_tenses():
    verbs = get_test_verbs()
    assert len(verbs) > 0
    assert get_tenses(verbs) == ["present", "futur", "imparfait"]


def test_get_groups():
    verbs = get_test_verbs()
    assert len(verbs) > 0
    assert get_groups(verbs) == ["1", "2", "3", "4", "0"]


def test_filter_tense():
    verbs = get_test_verbs()
    assert len(verbs) > 0
    filtered_verbs = filter_tense("present", verbs)
    for verb in filtered_verbs:
        assert verb["tense"] == "present"


def test_filter_group():
    verbs = get_test_verbs()
    assert len(verbs) > 0
    filtered_verbs = filter_group("2", verbs)
    for verb in filtered_verbs:
        assert verb["group"] == "2"


def test_filter_person():
    verbs = get_test_verbs()
    assert len(verbs) > 0
    filtered_verbs = filter_person("3", verbs)
    for verb in filtered_verbs:
        assert verb["person"] == "3"


def test_choose_question():
    assert choose_question("amo", "j'aime", "latin") == ("amo", "j'aime", "French")
    assert choose_question("amo", "j'aime", "french") == ("j'aime", "amo", "Latin")


#def test_ask_verb():


def test_get_language_answer():
    assert get_language_answer("latin") == "french"
    assert get_language_answer("french") == "latin"
    with pytest.raises(ValueError):
        get_language_answer("français")


def test_get_all_answers():
    verbs = get_test_verbs()
    assert len(verbs) > 0
    assert get_all_answers(verbs, "j'aime", "french", "latin") == ["amo"]
    assert get_all_answers(verbs, "lego", "latin", "french") == ["je lis", "je cueille", "je choisis"]


def test_compare_answers():
    assert compare_answers("amo", ["amo"], "latin") == True
    assert compare_answers("ammo", ["amo"], "latin") == False
    assert compare_answers("je choisis", ["je lis", "je cueille", "je choisis"], "french") == True
    assert compare_answers("jubebo", ["iubebo"], "latin") == True
    assert compare_answers("venio", ["uenio"], "latin") == True
    assert compare_answers("elle fait", ["il fait"], "french") == True
    assert compare_answers("Il fait", ["il fait"], "french") == True
    assert compare_answers("Elles donneront", ["ils donneront"], "french") == True


def test_get_hint():
    verbs = get_test_verbs()
    assert len(verbs) > 0
    chosen_verb = verbs[0]
    assert get_hint(chosen_verb, "french", 0) == None
    assert get_hint(chosen_verb, "latin", 0) == None
    assert get_hint(chosen_verb, "french", 1) == "amare"
    assert get_hint(chosen_verb, "latin", 1) == None
    assert get_hint(chosen_verb, "french", 2) == "amo, as, are, aui, atum"
    assert get_hint(chosen_verb, "latin", 2) == "aimer"
