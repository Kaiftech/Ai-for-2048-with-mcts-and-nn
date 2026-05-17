import unittest
from game2048 import Game2048

class TestGame2048(unittest.TestCase):
    def setUp(self):
        self.game = Game2048()

    def test_initialization(self):
        # A new game should have exactly two tiles initialized.
        # Since it is 4x4 grid, the total sum of tiles > 0 should be 2.
        nonzero_count = sum(1 for row in self.game.grid for cell in row if cell > 0)
        self.assertEqual(nonzero_count, 2)
        self.assertEqual(self.game.score, 0)
        self.assertFalse(self.game.done)
        self.assertEqual(self.game.moves_since_last_merge, 0)

    def test_reset(self):
        self.game.score = 100
        self.game.done = True
        self.game.moves_since_last_merge = 5
        self.game.reset()

        nonzero_count = sum(1 for row in self.game.grid for cell in row if cell > 0)
        self.assertEqual(nonzero_count, 2)
        self.assertEqual(self.game.score, 0)
        self.assertFalse(self.game.done)
        self.assertEqual(self.game.moves_since_last_merge, 0)

    def test_add_random_tile_empty(self):
        # Clear grid manually
        self.game.grid = [[0] * 4 for _ in range(4)]
        self.assertTrue(self.game.add_random_tile())

        nonzero_count = sum(1 for row in self.game.grid for cell in row if cell > 0)
        self.assertEqual(nonzero_count, 1)

    def test_add_random_tile_full(self):
        # Fill grid
        self.game.grid = [[2] * 4 for _ in range(4)]
        self.assertFalse(self.game.add_random_tile())

    def test_compress_row(self):
        test_cases = [
            ([2, 2, 0, 0], [4, 0, 0, 0], True),
            ([2, 0, 2, 0], [4, 0, 0, 0], True),
            ([2, 2, 4, 4], [4, 8, 0, 0], True),
            ([2, 4, 8, 16], [2, 4, 8, 16], False),
            ([0, 0, 0, 2], [2, 0, 0, 0], True),
            ([2, 2, 2, 2], [4, 4, 0, 0], True),
        ]

        for initial, expected_result, expected_changed in test_cases:
            result, changed = self.game.compress_row(initial)
            self.assertEqual(result, expected_result, f"Failed on {initial}")
            self.assertEqual(changed, expected_changed, f"Changed flag failed on {initial}")

    def test_move_left(self):
        self.game.grid = [
            [2, 2, 0, 0],
            [2, 0, 2, 0],
            [2, 2, 4, 4],
            [2, 4, 8, 16]
        ]
        changed = self.game.move_left(add_random=False)
        self.assertTrue(changed)
        expected_grid = [
            [4, 0, 0, 0],
            [4, 0, 0, 0],
            [4, 8, 0, 0],
            [2, 4, 8, 16]
        ]
        self.assertEqual(self.game.grid, expected_grid)

    def test_move_right(self):
        self.game.grid = [
            [2, 2, 0, 0],
            [2, 0, 2, 0],
            [2, 2, 4, 4],
            [2, 4, 8, 16]
        ]
        changed = self.game.move_right(add_random=False)
        self.assertTrue(changed)
        expected_grid = [
            [0, 0, 0, 4],
            [0, 0, 0, 4],
            [0, 0, 4, 8],
            [2, 4, 8, 16]
        ]
        self.assertEqual(self.game.grid, expected_grid)

    def test_move_up(self):
        self.game.grid = [
            [2, 2, 2, 2],
            [2, 0, 2, 4],
            [0, 2, 4, 8],
            [0, 0, 4, 16]
        ]
        changed = self.game.move_up(add_random=False)
        self.assertTrue(changed)
        expected_grid = [
            [4, 4, 4, 2],
            [0, 0, 8, 4],
            [0, 0, 0, 8],
            [0, 0, 0, 16]
        ]
        self.assertEqual(self.game.grid, expected_grid)

    def test_move_down(self):
        self.game.grid = [
            [2, 2, 2, 2],
            [2, 0, 2, 4],
            [0, 2, 4, 8],
            [0, 0, 4, 16]
        ]
        changed = self.game.move_down(add_random=False)
        self.assertTrue(changed)
        expected_grid = [
            [0, 0, 0, 2],
            [0, 0, 0, 4],
            [0, 0, 4, 8],
            [4, 4, 8, 16]
        ]
        self.assertEqual(self.game.grid, expected_grid)

    def test_get_legal_moves(self):
        self.game.grid = [
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 2048, 4096],
            [8192, 16384, 32768, 65536]
        ]
        # No empty cells and no adjacent equal tiles
        self.assertEqual(self.game.get_legal_moves(), [])

        self.game.grid = [
            [2, 2, 8, 16], # Can move left or right
            [32, 64, 128, 256],
            [512, 1024, 2048, 4096],
            [8192, 16384, 32768, 65536]
        ]
        # Since [0][0] and [0][1] are same, we can move left, right
        self.assertIn(2, self.game.get_legal_moves())
        self.assertIn(3, self.game.get_legal_moves())
        self.assertNotIn(0, self.game.get_legal_moves())
        self.assertNotIn(1, self.game.get_legal_moves())

    def test_is_done(self):
        # Empty cells exist
        self.game.grid = [[0] * 4 for _ in range(4)]
        self.assertFalse(self.game.is_done())

        # No empty cells, merge possible
        self.game.grid = [
            [2, 2, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 2048, 4096],
            [8192, 16384, 32768, 65536]
        ]
        self.assertFalse(self.game.is_done())

        # No empty cells, no merge possible
        self.game.grid = [
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 2048, 4096],
            [8192, 16384, 32768, 65536]
        ]
        self.assertTrue(self.game.is_done())

    def test_clone(self):
        self.game.grid = [
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 2048, 4096],
            [8192, 16384, 32768, 65536]
        ]
        self.game.score = 1000
        self.game.done = True
        self.game.moves_since_last_merge = 10

        cloned = self.game.clone()

        self.assertEqual(cloned.grid, self.game.grid)
        self.assertEqual(cloned.score, self.game.score)
        self.assertEqual(cloned.done, self.game.done)
        self.assertEqual(cloned.moves_since_last_merge, self.game.moves_since_last_merge)

        # Ensure deep copy
        self.game.grid[0][0] = 0
        self.assertNotEqual(cloned.grid[0][0], self.game.grid[0][0])

if __name__ == '__main__':
    unittest.main()
