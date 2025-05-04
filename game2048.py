import random

class Game2048:
    def __init__(self):
        self.reset()

    def reset(self):
        """Reset board to initial state with two tiles."""
        self.grid = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.done = False
        self.moves_since_last_merge = 0  # Track moves since last merge
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        """Add a random tile (2 or 4) to an empty cell."""
        empty = [(r, c) for r in range(4) for c in range(4) if self.grid[r][c] == 0]
        if not empty:
            return False
        r, c = random.choice(empty)
        self.grid[r][c] = 4 if random.random() < 0.1 else 2
        return True

    def compress_row(self, row):
        """Helper: compress a row to the left, merging equal tiles. Returns new row and changed flag."""
        new_row = [x for x in row if x != 0]
        changed = False
        i = 0
        while i < len(new_row) - 1:
            if new_row[i] == new_row[i + 1]:
                new_row[i] *= 2
                self.score += new_row[i]
                new_row.pop(i + 1)
                new_row.append(0)
                changed = True
                self.moves_since_last_merge = 0  # Reset the counter after a merge
            i += 1
        # Pad with zeros on the right
        new_row2 = [x for x in new_row if x != 0]
        new_row2 += [0] * (4 - len(new_row2))
        if new_row2 != row:
            changed = True
        return new_row2, changed

    def move_left(self, add_random=True):
        """Move all tiles left. If any tile moves or merges, add a random tile."""
        changed_any = False
        for r in range(4):
            new_row, changed = self.compress_row(self.grid[r])
            if changed:
                changed_any = True
            self.grid[r] = new_row
        if changed_any and add_random:
            self.add_random_tile()
        return changed_any

    def move_right(self, add_random=True):
        """Move all tiles right."""
        changed_any = False
        for r in range(4):
            reversed_row = list(reversed(self.grid[r]))
            new_row, changed = self.compress_row(reversed_row)
            new_row.reverse()
            if changed:
                changed_any = True
            self.grid[r] = new_row
        if changed_any and add_random:
            self.add_random_tile()
        return changed_any

    def move_up(self, add_random=True):
        """Move all tiles up."""
        changed_any = False
        # Transpose to reuse left-move logic
        self.grid = [list(row) for row in zip(*self.grid)]
        for r in range(4):
            new_row, changed = self.compress_row(self.grid[r])
            if changed:
                changed_any = True
            self.grid[r] = new_row
        self.grid = [list(row) for row in zip(*self.grid)]
        if changed_any and add_random:
            self.add_random_tile()
        return changed_any

    def move_down(self, add_random=True):
        """Move all tiles down."""
        changed_any = False
        self.grid = [list(row) for row in zip(*self.grid)]
        for r in range(4):
            reversed_row = list(reversed(self.grid[r]))
            new_row, changed = self.compress_row(reversed_row)
            new_row.reverse()
            if changed:
                changed_any = True
            self.grid[r] = new_row
        self.grid = [list(row) for row in zip(*self.grid)]
        if changed_any and add_random:
            self.add_random_tile()
        return changed_any

    def get_legal_moves(self):
        """Return a list of legal moves (directions 0=up,1=down,2=left,3=right)."""
        moves = []
        # Check each direction by simulating (without adding a new tile)
        temp = Game2048()
        temp.grid = [row[:] for row in self.grid]
        if temp.move_up(add_random=False):
            moves.append(0)
        temp.grid = [row[:] for row in self.grid]
        if temp.move_down(add_random=False):
            moves.append(1)
        temp.grid = [row[:] for row in self.grid]
        if temp.move_left(add_random=False):
            moves.append(2)
        temp.grid = [row[:] for row in self.grid]
        if temp.move_right(add_random=False):
            moves.append(3)
        return moves

    def is_done(self):
        """Check if no moves are possible."""
        # If any empty, not done
        for row in self.grid:
            if 0 in row:
                return False
        # If any merge possible, not done
        for r in range(4):
            for c in range(4):
                val = self.grid[r][c]
                if (r < 3 and self.grid[r + 1][c] == val) or (c < 3 and self.grid[r][c + 1] == val):
                    return False
        return True

    def clone(self):
        """Return a deep copy of this game (for MCTS simulations)."""
        new_game = Game2048()
        new_game.grid = [row[:] for row in self.grid]
        new_game.score = self.score
        new_game.done = self.done
        new_game.moves_since_last_merge = self.moves_since_last_merge  # Copy the counter
        return new_game
