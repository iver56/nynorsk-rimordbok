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
        