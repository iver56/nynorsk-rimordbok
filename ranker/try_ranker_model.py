import os

import joblib
import numpy as np

from ranker.make_samples import DATASET_DIR
from ranker.train import Vectorizer

if __name__ == "__main__":
    os.makedirs(DATASET_DIR, exist_ok=True)

    vectorizer = Vectorizer(mode="prediction")
    model = joblib.load(Vectorizer.MODEL_FILE_PATH)

    while True:
        print("Provide three words:")
        search_word = input("Search word > ")
        first_rhyme_candidate = input("First rhyme candidate > ")
        second_rhyme_candidate = input("Second rhyme candidate > ")

        triplet = {
            "search_word": search_word,
            "first_rhyme_candidate": first_rhyme_candidate,
            "second_rhyme_candidate": second_rhyme_candidate,
        }

        input_vector = vectorizer.vectorize_triplet(triplet).ravel()
        predicted_ranks = model.predict(np.array([input_vector]))
        predicted_rank = predicted_ranks[0]
        print(predicted_rank)
        if predicted_rank < 0:
            print("{} is preferred".format(first_rhyme_candidate))
        elif predicted_rank == 0.0:
            print("Both rhymes are considered equally good")
        else:
            print("{} is preferred".format(second_rhyme_candidate))
