from syllable_counter.syllable_dataset import (
    SYLLABLE_COUNT_EXAMPLES,
    HIATUS_WORDS,
    DIPHTHONG_WORDS,
)


def count_syllables(word, use_lookup=True):
    if use_lookup and word in SYLLABLE_COUNT_EXAMPLES:
        return SYLLABLE_COUNT_EXAMPLES[word]

    word = word.lower()

    word = word.replace("á", "a")
    word = word.replace("à", "a")
    word = word.replace("ó", "o")
    word = word.replace("ò", "o")

    for hiatus_word in HIATUS_WORDS:
        if hiatus_word in word:
            word = word.replace(hiatus_word, HIATUS_WORDS[hiatus_word])

    for diphthong_word in DIPHTHONG_WORDS:
        if diphthong_word in word:
            word = word.replace(diphthong_word, DIPHTHONG_WORDS[diphthong_word])

    word = word.replace("ai", "ä")
    word = word.replace("ei", "ë")
    word = word.replace("au", "â")
    word = word.replace("øy", "ö")
    word = word.replace("oi", "ô")
    word = word.replace("oy", "ô")

    syllable_map = map(word.lower().count, "aeiouyæøåäëâöô")
    syllable_sum = sum(syllable_map)
    return syllable_sum


if __name__ == "__main__":
    """Run this script to evaluate the syllable counter against a list of ground truths."""
    num_correct = 0
    total_num_words = len(SYLLABLE_COUNT_EXAMPLES)
    for word in SYLLABLE_COUNT_EXAMPLES:
        predicted_num_syllables = count_syllables(word, use_lookup=False)
        ground_truth_num_syllables = SYLLABLE_COUNT_EXAMPLES[word]
        if predicted_num_syllables == ground_truth_num_syllables:
            num_correct += 1
        else:
            print(
                "{} was classified incorrectly. Expected {} syllables, but got {}.".format(
                    word, ground_truth_num_syllables, predicted_num_syllables
                )
            )

    accuracy = num_correct / total_num_words
    print("Accuracy: {:.4f}".format(accuracy))
