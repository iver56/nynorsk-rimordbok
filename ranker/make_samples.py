import os
import joblib
import random
import uuid

from app.rhyme import get_rhymes
from app.settings import DATA_DIR
from app.utils import get_words


DATASET_DIR = DATA_DIR / "ranker_dataset"


def save_example(search_word, first_rhyme_candidate, second_rhyme_candidate, rank):
    """
    :param search_word:
    :param first_rhyme_candidate:
    :param second_rhyme_candidate:
    :param rank: -1 means 1st candidate is deemed best, 1 means 2nd candidate is deemed best,
        0 means they are deemed equal
    :return:
    """
    data = {
        "search_word": search_word,
        "first_rhyme_candidate": first_rhyme_candidate,
        "second_rhyme_candidate": second_rhyme_candidate,
        "rank": rank,
    }

    filename = str(uuid.uuid4()) + ".pkl"
    joblib.dump(data, DATASET_DIR / filename)


if __name__ == "__main__":
    os.makedirs(DATASET_DIR, exist_ok=True)

    all_words = list(get_words())

    while True:
        search_word = random.choice(all_words)

        rhymes = get_rhymes(search_word)
        random_number = random.random()
        if random_number > 0.75:
            print("Provide three words:")
            search_word = input("Search word > ")
            first_rhyme_candidate = input("First rhyme candidate > ")
            second_rhyme_candidate = input("Second rhyme candidate > ")
        elif random_number > 0.5:
            print("Query: {}".format(search_word))
            print("Provide two words:")
            first_rhyme_candidate = input("First rhyme candidate > ")
            second_rhyme_candidate = input("Second rhyme candidate > ")
        elif random_number > 0.25:
            print("Query: {}".format(search_word))
            first_rhyme_candidate, second_rhyme_candidate = random.sample(rhymes, 2)
            first_rhyme_candidate = first_rhyme_candidate["word"]
            second_rhyme_candidate = second_rhyme_candidate["word"]
        else:
            print("Query: {}".format(search_word))
            first_rhyme_candidate = random.choice(all_words)
            second_rhyme_candidate = random.choice(all_words)

        print("{} | {}".format(first_rhyme_candidate, second_rhyme_candidate))
        answer = input(
            "Which is best? left (l), right (r), equal (e) or discard (d)\n> "
        )
        rank = 0
        if not answer or answer.startswith("d"):
            continue
        elif answer.startswith("e"):
            rank = 0
        elif answer.startswith("l"):
            rank = -1
        elif answer.startswith("r"):
            rank = 1
        elif answer.startswith("q"):
            print("Quitting")
            break
        else:
            print("Unknown command!")

        save_example(search_word, first_rhyme_candidate, second_rhyme_candidate, rank)
