import unittest

from app.rhyme import get_rhymes
from app.rhyme import get_random_word
from app.rhyme import prepare_string


class TestRhymes(unittest.TestCase):
    def test_get_rhymes(self):
        rhymes = get_rhymes("drueklase")
        self.assertGreater(len(rhymes), 1)
        rhyme_words = [rhyme["word"] for rhyme in rhymes]
        self.assertIn("fjase", rhyme_words)

        self.assertEqual(len(get_rhymes("asdfkuhrkjhsdf")), 0)

    def test_search_word_not_included(self):
        rhymes = get_rhymes("drueklase")
        rhyme_words = [rhyme["word"] for rhyme in rhymes]
        self.assertNotIn("drueklase", rhyme_words)

    def test_whitespace_in_search_word(self):
        rhymes = get_rhymes(" daggry ")
        rhyme_words = [rhyme["word"] for rhyme in rhymes]
        self.assertIn("gry", rhyme_words)

    def test_syllables_in_result(self):
        rhymes = get_rhymes("daggry")
        for rhyme in rhymes:
            if rhyme["word"] == "morgongry":
                self.assertEqual(3, rhyme["num_syllables"])

    def test_ranking_when_rhyme_ends_with_search_word(self):
        rhymes = get_rhymes("bark")
        sevjebark_rank = None
        gjerrigknark_rank = None
        for i, rhyme in enumerate(rhymes):
            if rhyme["word"] == "sevjebark":
                sevjebark_rank = i
            elif rhyme["word"] == "gjerrigknark":
                gjerrigknark_rank = i

        self.assertGreater(sevjebark_rank, gjerrigknark_rank)

    def test_case_insensitivity(self):
        rhymes = get_rhymes("gry")
        rhyme_words = [rhyme["word"] for rhyme in rhymes]
        self.assertNotIn("Gry", rhyme_words)

    def test_limit_number_of_results(self):
        rhymes = get_rhymes("kløver")
        self.assertLessEqual(len(rhymes), 500)

    def test_consider_4_last_letters(self):
        rhymes = get_rhymes("kjeksa")
        floyelsbuksa_rank = None
        trollheksa_rank = None
        for i, rhyme in enumerate(rhymes):
            if rhyme["word"] == "fløyelsbuksa":
                floyelsbuksa_rank = i
            elif rhyme["word"] == "trollheksa":
                trollheksa_rank = i

        self.assertGreater(floyelsbuksa_rank, trollheksa_rank)

    def test_get_random_word(self):
        word = get_random_word()
        self.assertGreater(len(word), 0)

    def test_prepare_string(self):
        word = prepare_string("markør")
        self.assertEqual("markør", word)
