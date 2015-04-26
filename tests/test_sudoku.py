__author__ = 'Tirth Patel <complaints@tirthpatel.com>'

import unittest
from sudoku import solver
import time


class TestSudoku(unittest.TestCase):
    def setUp(self):
        self.sudoku = solver.Sudoku(max_iterations=1000, debug_print=False)

        easy = ('830076042'
                '600300097'
                '000082100'
                '090030005'
                '026000730'
                '300020010'
                '003460000'
                '170003006'
                '260790054')

        medium = ('050000006'
                  '480090003'
                  '903800000'
                  '017004000'
                  '600172005'
                  '000500810'
                  '000003508'
                  '700050041'
                  '800000090')

        hard = ('003105060'
                '000004008'
                '060000507'
                '056000000'
                '094602150'
                '000000620'
                '509000040'
                '600400000'
                '040203900')

        evil = ('005090400'
                '700046000'
                '000300090'
                '600000020'
                '090158030'
                '080000009'
                '060005000'
                '000920001'
                '008010900')

        # complete
        done = ('391286574'
                '487359126'
                '652714839'
                '875431692'
                '213967485'
                '964528713'
                '149673258'
                '538142967'
                '726895341')

        # supposedly the world's hardest?
        everest = ('800000000'
                   '003600000'
                   '070090200'
                   '050007000'
                   '000045700'
                   '000100030'
                   '001000068'
                   '008500010'
                   '090000400')

        self.puzzle = evil  # choose puzzle

    def test_solve(self):
        self.assertTrue(self.sudoku.get_input(self.puzzle))
        self.assertTrue(self.sudoku.solve())
        print('done in', self.sudoku.current)

    def test_efficiency(self):
        iterations, times = [], []
        validity = 100

        for i in range(validity):
            if self.sudoku.get_input(self.puzzle):
                start = time.clock()
                self.assertTrue(self.sudoku.solve())
                end = time.clock()

                times.append(end - start)

            progress = i / (validity / 100)
            if progress % 10.0 == 0.0:
                print(str(progress) + "%")

            iterations.append(self.sudoku.current)

            self.sudoku = solver.Sudoku(max_iterations=1000)
            self.sudoku.get_input(self.puzzle)

        print('--')
        print('after', len(iterations), 'runs')
        print('min iters:', str(min(iterations)) + ',',
              'max iters:', max(iterations))
        print('min time: ', str(round(min(times) * 1000, 2)) + ',',
              'max time:', round(max(times) * 1000, 2))
        print('average iters:', sum(iterations) / len(iterations))
        print('average time: ', round((sum(times) / len(times) * 1000), 2))


if __name__ == '__main__':
    unittest.main(exit=False)