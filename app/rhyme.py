# -*- coding: utf-8 -*-

import re
import random
from functools import lru_cache

from app.utils import get_words
from syllable_counter.algorithm import count_syllables


@lru_cache(maxsize=9001)
def get_rhymes(word):
    word = prepare_string(word).strip()
    assert type(word) == str
    assert len(word) >= 1
    words = get_words()

    rhymes = []
    max_ending_size = min(4, len(word))
    max_ending = word[-max_ending_size:]
    smaller_ending_size = max(1, max_ending_size - 1)
    smaller_ending = word[-smaller_ending_size:]
    for candidate_word in words:
        candidate_word_lower = prepare_string(candidate_word)
        if candidate_word_lower == word:
            # Discard, because we don't want to include the search word in the results
            continue

        if candidate_word_lower.endswith(smaller_ending):
            num_syllables = count_syllables(candidate_word)
            rhyme = {"word": candidate_word, "score": 100, "num_syllables": num_syllables}

            if candidate_word_lower.endswith(max_ending):
                rhyme['score'] *= 2

            if candidate_word.lower().endswith(word):
                rhyme["score"] *= 0.3

            rhymes.append(rhyme)

    rhymes.sort(key=lambda rhyme: rhyme["score"], reverse=True)

    # Limit the number of words in the result
    rhymes = rhymes[0:500]

    return rhymes


def prepare_string(word):
    # remove non-alphabetic characters from string
    return re.sub(r'[\.\-\"\'\/@#$%&\(\)]', '', word.lower())


def get_random_word():
    words = get_words()
    chosen_word = random.choice(words)
    return chosen_word
