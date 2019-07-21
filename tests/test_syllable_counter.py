# -*- coding: utf-8 -*-

import unittest

from syllable_counter.algorithm import count_syllables
from syllable_counter.syllable_dataset import SYLLABLE_COUNT_EXAMPLES


class TestSyllableCounter(unittest.TestCase):
    def test_syllable_counter(self):
        for word in SYLLABLE_COUNT_EXAMPLES:
            predicted_num_syllables = count_syllables(word)
            ground_truth_num_syllables = SYLLABLE_COUNT_EXAMPLES[word]
            assert predicted_num_syllables == ground_truth_num_syllables
