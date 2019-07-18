# -*- coding: utf-8 -*-

import unittest

from app.rhyme import get_rhymes
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
        rhyme_candidates = ["klokkeslett", "pang", "kransekake"]

        ranker = Ranker()
        ranked_rhymes = ranker.rank_rhymes(search_word, rhymes=rhyme_candidates)
        self.assertEqual(ranked_rhymes, ["pang", "kransekake", "klokkeslett"])
