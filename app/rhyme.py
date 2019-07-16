# -*- coding: utf-8 -*-

from functools import lru_cache

from app.utils import get_words


@lru_cache(maxsize=9001)
def get_rhymes(word):
    word = word.strip().lower()
    assert type(word) == str
    assert len(word) >= 1
    words = get_words()

    rhymes = []
    ending_size = min(3, len(word))
    ending = word[-ending_size:]
    for candidate_word in words:
        candidate_word_lower = candidate_word.lower()
        if candidate_word_lower.endswith(ending) and candidate_word_lower != word:
            word_syllables = get_syllables(candidate_word)
            rhyme = {"word": candidate_word, "score": 100, "syllables": word_syllables}
            if candidate_word.lower().endswith(word):
                rhyme["score"] *= 0.5
            rhymes.append(rhyme)

    rhymes.sort(key=lambda rhyme: rhyme["score"], reverse=True)

    # Limit the number of words in the result
    rhymes = rhymes[0:500]

    return rhymes


def get_syllables(word):
    syllable_map = map(word.lower().count, "aeiouyæøå")
    syllable_sum = sum(syllable_map)
    return syllable_sum
