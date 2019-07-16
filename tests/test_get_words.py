import unittest

from app.utils import get_words


class TestGetWords(unittest.TestCase):
    def test_get_words(self):
        words = get_words()
        self.assertGreater(len(words), 400000)
