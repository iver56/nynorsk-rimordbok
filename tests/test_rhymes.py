import unittest

from app.rhyme import get_rhymes


class TestRhymes(unittest.TestCase):
    def test_get_rhymes(self):
        rhymes = get_rhymes("klase")
        self.assertGreater(len(rhymes), 1)
        rhyme_words = [rhyme["word"] for rhyme in rhymes]
        self.assertIn("tofase", rhyme_words)

        self.assertEqual(len(get_rhymes("asdfkuhriu")), 0)
