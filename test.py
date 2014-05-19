# coding=utf-8
import unittest
import sys
import os
from game import Board, Game, random_strategy, minimax_strategy


class BoardTest(unittest.TestCase):
    def setUp(self):
        self.b = Board()

    def test_row_win(self):
        self.assertFalse(self.b.finished())
        self.assertTrue(self.b.move(0, 0, 'x'))
        self.assertFalse(self.b.finished())
        self.assertTrue(self.b.move(0, 2, 'x'))
        self.assertFalse(self.b.finished())
        self.assertFalse(self.b.move(0, 'as', 'x'))
        self.assertFalse(self.b.move(0, 4, 'x'))
        self.assertFalse(self.b.move(4, 0, 'o'))
        self.assertFalse(self.b.move(0, 0, 'o'))
        self.assertFalse(self.b.finished())
        self.assertTrue(self.b.move(0, 1, 'x'))
        self.assertEqual(self.b.finished(), 1)

    def test_col_win(self):
        self.assertTrue(self.b.move(0, 1, 'o'))
        self.assertFalse(self.b.finished())
        self.assertTrue(self.b.move(1, 1, 'o'))
        self.assertFalse(self.b.finished())
        self.assertTrue(self.b.move(2, 1, 'o'))
        self.assertEqual(self.b.finished(), 1)

    def test_first_diag_win(self):
        self.assertTrue(self.b.move(0, 0, 'o'))
        self.assertFalse(self.b.finished())
        self.assertTrue(self.b.move(1, 1, 'o'))
        self.assertFalse(self.b.finished())
        self.assertTrue(self.b.move(2, 2, 'o'))
        self.assertEqual(self.b.finished(), 1)

    def test_second_diag_win(self):
        self.assertTrue(self.b.move(0, 2, 'o'))
        self.assertFalse(self.b.finished())
        self.assertTrue(self.b.move(1, 1, 'o'))
        self.assertFalse(self.b.finished())
        self.assertTrue(self.b.move(2, 0, 'o'))
        self.assertEqual(self.b.finished(), 1)

    def test_draw(self):
        self.assertTrue(self.b.move(0, 0, 'x'))
        self.assertFalse(self.b.finished())
        self.assertTrue(self.b.move(0, 1, 'o'))
        self.assertFalse(self.b.finished())
        self.assertTrue(self.b.move(0, 2, 'x'))
        self.assertTrue(self.b.move(1, 0, 'o'))
        self.assertFalse(self.b.finished())
        self.assertTrue(self.b.move(1, 1, 'x'))
        self.assertFalse(self.b.finished())
        self.assertTrue(self.b.move(1, 2, 'o'))
        self.assertTrue(self.b.move(2, 0, 'o'))
        self.assertFalse(self.b.finished())
        self.assertTrue(self.b.move(2, 1, 'x'))
        self.assertFalse(self.b.finished())
        self.assertTrue(self.b.move(2, 2, 'o'))
        self.assertEqual(self.b.finished(), 2)

    def test_all_filled_and_win(self):
        self.assertTrue(self.b.move(0, 0, 'x'))
        self.assertFalse(self.b.finished())
        self.assertTrue(self.b.move(0, 1, 'o'))
        self.assertFalse(self.b.finished())
        self.assertTrue(self.b.move(0, 2, 'x'))
        self.assertTrue(self.b.move(1, 0, 'o'))
        self.assertFalse(self.b.finished())
        self.assertTrue(self.b.move(1, 1, 'x'))
        self.assertFalse(self.b.finished())
        self.assertTrue(self.b.move(1, 2, 'o'))
        self.assertTrue(self.b.move(2, 0, 'o'))
        self.assertFalse(self.b.finished())
        self.assertTrue(self.b.move(2, 1, 'o'))
        self.assertFalse(self.b.finished())
        self.assertTrue(self.b.move(2, 2, 'o'))
        self.assertEqual(self.b.finished(), 1)


class GameTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stdout = sys.stdout
        null = open(os.devnull, 'wb')
        sys.stdout = null

    def test_random_strategies_3x3_board(self):
        # mainly test that everything run without error
        try:
            results = [0, 0, 0]
            for _ in range(1000):
                game = Game(random_strategy, random_strategy, 3)
                res = game.play()
                results[res] += 1
        except BaseException:
            self.fail("There was an error when 2 random strategies played on 3x3 board!")
        # also check that all outcomes are possible
        self.assertGreater(results[0], 20)
        self.assertGreater(results[1], 20)
        self.assertGreater(results[2], 20)

    def test_random_strategies_6x6_board(self):
        try:
            for _ in range(100):
                game = Game(random_strategy, random_strategy, 6)
                game.play()
        except BaseException:
            self.fail("There was an error when 2 random strategies played on 6x6 board!")

    def test_random_vs_minimax(self):
        try:
            results = [0, 0, 0]
            for _ in range(20):
                game = Game(random_strategy, minimax_strategy, 3)
                res = game.play()
                results[res] += 1
        except BaseException:
            self.fail("There was an error when random played vs minimax!")
        # random can't win
        self.assertEqual(results[1], 0)

    def test_minimax_vs_minimax(self):
        try:
            game = Game(minimax_strategy, minimax_strategy, 3)
            # must be a draw
            self.assertEqual(game.play(), 0)
        except BaseException:
            self.fail("There was an error when minimax played vs minimax!")

    @classmethod
    def tearDownClass(cls):
        sys.stdout = cls.stdout


if __name__ == '__main__':
    unittest.main()
