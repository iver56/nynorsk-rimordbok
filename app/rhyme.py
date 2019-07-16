from app.utils import get_words


def get_rhymes(word):
    assert type(word) == str
    assert len(word) >= 1

    words = get_words()

    rhymes = []
    ending_size = min(3, len(word))
    ending = word[-ending_size:]
    for word in words:
        if word.endswith(ending):
            rhymes.append({"word": word, "score": 100})

    return rhymes
