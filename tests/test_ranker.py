# -*- coding: utf-8 -*-

import unittest

from ranker.train import Vectorizer


class TestRankerPrepareData(unittest.TestCase):
    def test_slice_and_pad_words(self):
        vectorizer = Vectorizer(mode="dummy")
        self.assertEqual(vectorizer.preprocess_word("halloen"), "LLOEN")
        self.assertEqual(vectorizer.preprocess_word("ætt"), "  ÆTT")
