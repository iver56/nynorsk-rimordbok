import unittest

from app.rhyme import get_rhymes


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
                self.assertIn(3, [rhyme["syllables"]])

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
