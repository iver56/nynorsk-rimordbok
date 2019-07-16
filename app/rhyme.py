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
        if candidate_word.lower().endswith(ending) and candidate_word != word:
            rhymes.append({"word": candidate_word, "score": 100})

    return rhymes
