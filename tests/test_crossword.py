__author__ = 'Tirth Patel <complaints@tirthpatel.com>'

import unittest
from os import path
import crossword.solver as sol


class TestCrossword(unittest.TestCase):
    def setUp(self):
        pass

    def test_something(self):
        cells = 13

        sample_puzzle = path.realpath('..') + '\\crossword.txt'
        sample_answers = path.realpath('..') + '\\answers.json'

        across, down = sol.read_guardian_puzzle(sample_puzzle)
        crossword = sol.Crossword(cells, across, down, sample_answers)

        crossword.fill_answers()

        self.assertNotEqual((sum(line.count(sol.delimiter)
                                 for line in crossword.puzzle)), 63)

        while not crossword.fill_answers():
            crossword.fill_clues(None, None, True)  # reset and shuffle

        self.assertEqual((sum(line.count(sol.delimiter)
                              for line in crossword.puzzle)), 63)

        self.assertEqual(sum(len(a) for a in crossword.answers),
                         sum(c.length for c in crossword.clues))


if __name__ == '__main__':
    unittest.main(exit=False)
