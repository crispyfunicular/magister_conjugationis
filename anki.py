from project import *
import sys
import argparse
import genanki


def create_model():
    """
    *Output*
    model = format of the Anki cards
    """
    model = genanki.Model(
        1581981852,
        'Simple Model',
        fields=[
            {'name': 'Question'},
            {'name': 'Answer'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '<h2><center>{{Question}}</center></h2>',
                'afmt': '{{FrontSide}}<hr id="answer"><center>{{Answer}}</center>',
            },
        ])
    return model


def create_note(model, question, answer):
    """
    *Input* (three)
    model = format of the Anki cards
    question (str) = Latin verb to be asked
    answer (str) = French verb expected as answer

    *Output*
    note = an Anki card/note
    """
    note = genanki.Note(
        model = model,
        fields=[question, answer]
    )
    return note


def create_notes(model, verbs):
    """
    *Input* (two)
    model = format of the Anki cards
    verbs = list of dict

    *Output* (one)
    notes (list) = list of Anki cards/notes, one per verb
    """
    notes = []
    for verb in verbs:
        note = create_note(model, verb["french"], verb["latin"])
        notes.append(note)
    return notes


def create_deck(notes):
    """
    *Input*
    notes = list of Anki cards/notes, one per verb

    *Output* (one)
    deck = an Anki deck
    """
    deck = genanki.Deck(
        2114781006,
        "Latin verbs")
    for note in notes:
        deck.add_note(note)
    print("Cards added to the deck:", len(notes))
    return deck


def save_deck(deck, filename):
    """
    *Input* (two)
    deck = an Anki deck
    filename = filename of the package (.apkg)
    """
    print("Saving deck to", filename)
    genanki.Package(deck).write_to_file(filename)


def main():

    ###
    # Get CLI params
    ###

    parser = argparse.ArgumentParser(
                    prog='anki.py',
                    description='Creates French-Latin verbs Anki decks',
                    epilog='Bonam fortunam!')
    parser.add_argument('-i', '--input', type=str, default="verbs_latin.csv", help="Input filename of the csv list of verbs")
    parser.add_argument('-o', '--output', type=str, default="latin_verbs.apkg", help="Output filename of the Anki deck")
    args = parser.parse_args()

    input_filename = args.input
    output_filename = args.output


    ###
    # Load CSV file
    ###

    verbs_latin_csv = input_filename
    try:
        verbs = get_verbs(verbs_latin_csv)
    except FileNotFoundError:
        print("File not found")
        sys.exit(1)


    model = create_model()
    notes = create_notes(model, verbs)
    deck = create_deck(notes)
    save_deck(deck, output_filename)


if __name__ == "__main__":
    main()
