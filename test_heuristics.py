import unittest
from heuristics import monotonicity

class TestHeuristics(unittest.TestCase):

    def test_monotonicity_max(self):
        # Grid where values are always decreasing both horizontally and vertically
        grid = [
            [16, 15, 14, 13],
            [12, 11, 10,  9],
            [ 8,  7,  6,  5],
            [ 4,  3,  2,  1]
        ]
        # 4 rows * 3 comparisons = 12
        # 4 cols * 3 comparisons = 12
        # Total = 24
        self.assertEqual(monotonicity(grid), 24)

    def test_monotonicity_min(self):
        # Grid where values are always strictly increasing both horizontally and vertically
        grid = [
            [ 1,  2,  3,  4],
            [ 5,  6,  7,  8],
            [ 9, 10, 11, 12],
            [13, 14, 15, 16]
        ]
        # 0 true comparisons
        self.assertEqual(monotonicity(grid), 0)

    def test_monotonicity_mixed(self):
        # Grid with mixed monotonicity
        grid = [
            [ 4,  2,  4,  2], # 4>=2 (T), 2>=4 (F), 4>=2 (T) -> 2
            [ 2,  4,  2,  4], # 2>=4 (F), 4>=2 (T), 2>=4 (F) -> 1
            [ 4,  2,  4,  2], # -> 2
            [ 2,  4,  2,  4]  # -> 1
        ]
        # Rows sum = 6
        # Cols sum = 6 (cols are same as rows)
        # Total = 12
        self.assertEqual(monotonicity(grid), 12)

if __name__ == '__main__':
    unittest.main()
