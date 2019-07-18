from functools import cmp_to_key

import joblib

from ranker.train import Vectorizer

import numpy as np


class Ranker:
    def __init__(self):
        self.vectorizer = Vectorizer(mode="prediction")
        self.model = joblib.load(Vectorizer.MODEL_FILE_PATH)

    def rank_rhymes(self, search_word, rhymes):
        def compare(first_rhyme_candidate, second_rhyme_candidate):
            triplet = {
                "search_word": search_word,
                "first_rhyme_candidate": first_rhyme_candidate,
                "second_rhyme_candidate": second_rhyme_candidate,
            }
            flipped_triplet = {
                "search_word": search_word,
                "first_rhyme_candidate": second_rhyme_candidate,
                "second_rhyme_candidate": first_rhyme_candidate,
            }

            input_vector = self.vectorizer.vectorize_triplet(triplet).ravel()
            flipped_input_vector = self.vectorizer.vectorize_triplet(flipped_triplet).ravel()
            predicted_ranks = self.model.predict(np.array([input_vector, flipped_input_vector]))
            predicted_rank = predicted_ranks[0]
            other_predicted_rank = -predicted_ranks[1]
            predicted_rank = (predicted_rank + other_predicted_rank) / 2

            if predicted_rank < 0:
                print("{} is preferred".format(first_rhyme_candidate))
            elif predicted_rank == 0.0:
                print("Both rhymes are considered equally good")
            else:
                print("{} is preferred".format(second_rhyme_candidate))

            return predicted_rank

        rhymes.sort(key=cmp_to_key(compare), reverse=True)
        return rhymes
