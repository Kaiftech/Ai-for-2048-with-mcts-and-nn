import unittest
from heuristics import count_empty_tiles

class TestHeuristics(unittest.TestCase):

    def test_count_empty_tiles_all_zeros(self):
        grid = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.assertEqual(count_empty_tiles(grid), 16)

    def test_count_empty_tiles_no_zeros(self):
        grid = [
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 2048, 4096],
            [2, 4, 8, 16]
        ]
        self.assertEqual(count_empty_tiles(grid), 0)

    def test_count_empty_tiles_mixed(self):
        grid = [
            [2, 0, 8, 0],
            [0, 64, 0, 256],
            [512, 0, 2048, 0],
            [0, 4, 0, 16]
        ]
        self.assertEqual(count_empty_tiles(grid), 8)

    def test_count_empty_tiles_empty_grid(self):
        grid = []
        self.assertEqual(count_empty_tiles(grid), 0)

if __name__ == '__main__':
    unittest.main()
