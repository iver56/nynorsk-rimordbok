import os
from zipfile import ZipFile

from app.settings import DATA_DIR


def get_words():
    if not os.path.isfile(DATA_DIR / "fullform_nn.txt"):
        zip_ref = ZipFile(DATA_DIR / "ordbank_nn.zip", "r")
        zip_ref.extractall(DATA_DIR)
        zip_ref.close()

    words = set()

    with open(DATA_DIR / "fullform_nn.txt", "r") as words_file:
        for line in words_file.readlines():
            if line.startswith("*") or len(line) < 3:
                continue
            cells = line.split("\t")
            word = cells[2]
            words.add(word)

    return words
