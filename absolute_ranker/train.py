import copy
import json
import os
from pathlib import Path

import joblib
import numpy as np
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.model_selection import KFold
from sklearn.neighbors import KNeighborsRegressor
from tqdm import tqdm

from absolute_ranker.make_samples import DATASET_DIR
from app.settings import DATA_DIR
from ranker.utils import get_pickle_paths


def get_untrained_model(input_dim, model_type):
    # Create model
    if model_type == "knn":
        model = KNeighborsRegressor(weights="distance", n_neighbors=5)
    elif model_type == "et":
        model = ExtraTreesRegressor(n_estimators=10)
    else:
        raise Exception("Unknown model type")
    return model


class Vectorizer(object):
    METADATA_FILE_PATH = os.path.join(DATA_DIR / "absolute_ranker_model" / "metadata.json")
    MODEL_FILE_PATH = os.path.join(DATA_DIR / "absolute_ranker_model" / "model.pkl")
    MAX_STRING_LENGTH = 5  # the last characters of the word, not the first

    def __init__(self, mode="training"):
        dataset = None
        if mode == "training":
            dataset = get_dataset()
            search_words = [
                self.preprocess_word(example["search_word"]) for example in dataset
            ]
            rhyme_candidates = [
                self.preprocess_word(example["rhyme_candidate"])
                for example in dataset
            ]
            characters = (
                set("".join(search_words))
                .union(set("".join(rhyme_candidates)))
            )
            ordered_characters = sorted(list(characters))
            print("Characters: {}".format(ordered_characters))
            self.character_to_index = {
                character: index for index, character in enumerate(ordered_characters)
            }

            os.makedirs(Path(self.METADATA_FILE_PATH).parent, exist_ok=True)
            with open(self.METADATA_FILE_PATH, "w") as outfile:
                json.dump({"character_to_index": self.character_to_index}, outfile)
        elif mode == "prediction":
            with open(self.METADATA_FILE_PATH) as data_file:
                metadata = json.load(data_file)
            self.character_to_index = metadata["character_to_index"]
        else:
            # Dummy data for unit tests
            self.character_to_index = {}

        self.num_characters = len(self.character_to_index)

        if mode == "training":
            self.train_model(dataset)

    def train_model(self, dataset):
        input_vectors = [self.vectorize_pair(example) for example in dataset]
        target_vectors = [example["score"] for example in dataset]

        assert len(input_vectors) == len(target_vectors)

        num_examples = len(input_vectors)

        x = np.array(input_vectors).reshape((num_examples, -1))
        y = np.array(target_vectors).reshape((num_examples, 1))

        input_dim = x.shape[1]

        print("x shape", x.shape)
        print("y shape", y.shape)

        should_evaluate = True
        model_type = "et"
        if should_evaluate:
            kf = KFold(n_splits=10, shuffle=True)
            accuracies = []
            mean_absolute_errors = []
            for train_index, test_index in tqdm(kf.split(x), "Evaluating..."):
                X_train, X_test = x[train_index], x[test_index]
                y_train, y_test = y[train_index], y[test_index]

                model = get_untrained_model(input_dim, model_type)
                if model_type == "et":
                    model.fit(X_train, y_train.ravel())
                else:
                    model.fit(X_train, y_train)

                y_predictions = model.predict(X_test)

                num_correct_examples = 0
                num_examples = len(y_predictions)

                absolute_errors = []

                for i, y_prediction in enumerate(y_predictions):
                    y_prediction = float(y_prediction)
                    absolute_error = abs(y_prediction - y_test[i][0])
                    absolute_errors.append(absolute_error)
                    y_prediction = max(-1.0, y_prediction)
                    y_prediction = min(1.0, y_prediction)
                    y_prediction = round(y_prediction)
                    if y_prediction == y_test[i][0]:
                        num_correct_examples += 1

                mean_absolute_error = np.mean(absolute_errors)
                mean_absolute_errors.append(mean_absolute_error)

                accuracy = num_correct_examples / num_examples
                accuracies.append(accuracy)

            print("\nMean absolute error", np.mean(mean_absolute_errors))
            print("\nMean validation accuracy", np.mean(accuracies))

        # Fit model on all data
        model = get_untrained_model(input_dim, model_type)
        if model_type == "et":
            model.fit(x, y.ravel())
            joblib.dump(model, self.MODEL_FILE_PATH)
        else:
            model.fit(x, y)
            joblib.dump(model, self.MODEL_FILE_PATH)

    def preprocess_word(self, s):
        """Keep the last characters and left pad the strings if they are too short."""
        return s.upper()[-self.MAX_STRING_LENGTH :].rjust(self.MAX_STRING_LENGTH)

    def vectorize_string(self, s):
        s = self.preprocess_word(s)

        vectors = []
        for c in s:
            vector = [0] * self.num_characters
            character_index = self.character_to_index.get(c, None)
            if character_index is not None:
                vector[character_index] = 1
            vectors.append(vector)
        return vectors

    def vectorize_pair(self, rhyme_ranking_object):
        search_word_vector = self.vectorize_string(rhyme_ranking_object["search_word"])
        rhyme_candidate_vector = self.vectorize_string(
            rhyme_ranking_object["rhyme_candidate"]
        )

        input_vector = np.array(
            search_word_vector
            + rhyme_candidate_vector
        )
        return input_vector


def get_dataset():
    dataset = []
    file_paths = get_pickle_paths(DATASET_DIR)
    print("Found {} examples in the dataset".format(len(file_paths)))
    for file_path in file_paths:
        example = joblib.load(file_path)
        dataset.append(example)

        flipped_example = copy.deepcopy(example)
        flipped_example["search_word"] = example["rhyme_candidate"]
        flipped_example["rhyme_candidate"] = example["search_word"]
        dataset.append(flipped_example)

    return dataset


if __name__ == "__main__":
    Vectorizer(mode="training")
