# -*- coding: utf-8 -*-

import unittest

from ranker.apply_ranker_model import Ranker
from ranker.train import Vectorizer


class TestRankerPrepareData(unittest.TestCase):
    def test_slice_and_pad_words(self):
        vectorizer = Vectorizer(mode="dummy")
        self.assertEqual(vectorizer.preprocess_word("halloen"), "LLOEN")
        self.assertEqual(vectorizer.preprocess_word("ætt"), "  ÆTT")


class TestRanker(unittest.TestCase):
    def test_rank_rhymes(self):
        search_word = "rang"
        rhyme_candidates = ["gang", "klokkeslett", "pang", "kransekake", "sang"]

        ranker = Ranker()
        ranked_rhymes = ranker.rank_rhymes(search_word, rhymes=rhyme_candidates)
        self.assertIn(ranked_rhymes.index("sang"), (0, 1, 2))
        self.assertIn(ranked_rhymes.index("pang"), (0, 1, 2))
        self.assertIn(ranked_rhymes.index("gang"), (0, 1, 2))
        self.assertIn(ranked_rhymes.index("kransekake"), (3, 4))
        self.assertIn(ranked_rhymes.index("klokkeslett"), (3, 4))
