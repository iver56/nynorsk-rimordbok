import os
import joblib
import random
import uuid

from app.rhyme import get_rhymes
from app.settings import DATA_DIR
from app.utils import get_words


DATASET_DIR = DATA_DIR / "absolute_ranker_dataset"


def save_example(search_word, rhyme_candidate, score):
    """
    :param search_word:
    :param rhyme_candidate:
    :param score:
    * 1: not a rhyme
    * 2: letter rhyme
    * 3: bad rhyme
    * 4: good rhyme
    * 5: very good rhyme
    :return:
    """
    data = {
        "search_word": search_word,
        "rhyme_candidate": rhyme_candidate,
        "score": score,
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
            print("Provide two words:")
            search_word = input("Search word > ")
            rhyme_candidate = input("Rhyme candidate > ")
        elif random_number > 0.5:
            print("Query: {}".format(search_word))
            print("Provide a rhyme candidate:")
            rhyme_candidate = input("Rhyme candidate > ")
        elif random_number > 0.25:
            print("Query: {}".format(search_word))
            rhyme_candidate = random.choice(rhymes)
            rhyme_candidate = rhyme_candidate["word"]
        else:
            print("Query: {}".format(search_word))
            rhyme_candidate = random.choice(all_words)

        print("{}".format(rhyme_candidate))
        answer = input(
            "How good is the rhyme on a scale from 1 to 5? Alternatively, discard (d)\n> "
        )
        score = 0
        if not answer or answer.startswith("d"):
            continue
        elif answer in ("1", "2", "3", "4", "5"):
            score = int(answer)
        elif answer.startswith("q"):
            print("Quitting")
            break
        else:
            print("Unknown command!")

        save_example(search_word, rhyme_candidate, score)
