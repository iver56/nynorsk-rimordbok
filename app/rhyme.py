# -*- coding: utf-8 -*-

from functools import lru_cache

from app.utils import get_words

import re


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
            word_syllables = get_syllables(candidate_word)
            rhyme = {"word": candidate_word, "score": 100, "syllables": word_syllables}

            if candidate_word_lower.endswith(max_ending):
                rhyme['score'] *= 2

            if candidate_word.lower().endswith(word):
                rhyme["score"] *= 0.3

            rhymes.append(rhyme)

    rhymes.sort(key=lambda rhyme: rhyme["score"], reverse=True)

    # Limit the number of words in the result
    rhymes = rhymes[0:500]

    return rhymes


def get_syllables(word):
    syllable_map = map(word.lower().count, "aeiouyæøå")
    syllable_sum = sum(syllable_map)
    return syllable_sum

def prepare_string(word):
    # remove non-alphabetic characters from string
    return re.sub(r'[^a-zA-Z ]', '', word.lower())
