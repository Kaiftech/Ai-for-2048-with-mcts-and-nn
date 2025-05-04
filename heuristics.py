# heuristics.py

def count_empty_tiles(grid):
    """Count the number of empty tiles in the grid."""
    return sum(1 for row in grid for cell in row if cell == 0)

def monotonicity(grid):
    """Measure the monotonicity of the grid (row/column order)."""
    total = 0
    for row in grid:
        for i in range(3):
            if row[i] >= row[i+1]:
                total += 1
    for col in zip(*grid):
        for i in range(3):
            if col[i] >= col[i+1]:
                total += 1
    return total

def merge_potential(grid):
    """Measure the potential for merging tiles."""
    potential = 0
    for i in range(4):
        for j in range(4):
            if j < 3 and grid[i][j] == grid[i][j+1]:
                potential += 1
            if i < 3 and grid[i][j] == grid[i+1][j]:
                potential += 1
    return potential

def compute_fitness(game):
    grid = game.grid
    empty_tiles = count_empty_tiles(grid)
    monotonic = monotonicity(grid)
    merge_score = merge_potential(grid)
    actual_score = game.score

    # Reward for long-term strategy (higher score, fewer moves)
    long_term_score = 0
    if game.score > 1000:  # Example threshold for high performance
        long_term_score += 100

    # Penalty for stagnation
    stagnation_penalty = -50 if game.moves_since_last_merge > 10 else 0

    return actual_score + (empty_tiles * 10) + (monotonic * 5) + (merge_score * 20) + long_term_score + stagnation_penalty
