from app.utils import get_words


def get_rhymes(word):
    assert type(word) == str
    assert len(word) >= 1
    word = word.strip()
    words = get_words()

    rhymes = []
    ending_size = min(3, len(word))
    ending = word[-ending_size:]
    for candidate_word in words:
        if candidate_word.endswith(ending) and candidate_word != word:
            rhymes.append({"word": candidate_word, "score": 100})

    return rhymes
