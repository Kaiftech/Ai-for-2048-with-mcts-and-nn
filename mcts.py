import math
import torch
from game2048 import Game2048
from model import Model

class MCTSNode:
    def __init__(self, game: Game2048, prior=0, parent=None):
        self.game = game.clone()   # state at this node
        self.prior = prior         # prior probability (from parent policy)
        self.parent = parent
        self.children = {}         # map action->child node
        self.visit_count = 0
        self.value_sum = 0.0
        self.dynamic_c_puct = 1.0 # Dynamic c_puct adjustment
        self.is_terminal = game.is_done()

    def Q(self):
        if self.visit_count == 0:
            return 0
        return self.value_sum / self.visit_count

    def expand(self, policy_probs):
        """Expand node by creating children for all legal moves."""
        legal_moves = self.game.get_legal_moves()
        for a in legal_moves:
            if a not in self.children:
                next_game = self.game.clone()
                # Apply move on next_game (this also adds random tile)
                if a == 0:
                    next_game.move_up(add_random=True)
                elif a == 1:
                    next_game.move_down(add_random=True)
                elif a == 2:
                    next_game.move_left(add_random=True)
                elif a == 3:
                    next_game.move_right(add_random=True)
                child_node = MCTSNode(next_game, prior=policy_probs[a], parent=self)
                self.children[a] = child_node

    def backpropagate(self, value):
        """Backpropagate the value to all ancestors in the tree."""
        node = self
        while node is not None:
            node.visit_count += 1
            node.value_sum += value
            node = node.parent

class MCTS:
    def __init__(self, model: Model, num_simulations=50, c_puct=1.0):
        self.model = model
        self.num_simulations = num_simulations
        self.c_puct = c_puct

    def search(self, root_game: Game2048):
        """Run MCTS and return the best move for the root_game."""
        root = MCTSNode(root_game, prior=1.0)
        
        # Initial evaluation and expansion
        state = torch.tensor(self._state_to_tensor(root.game), dtype=torch.float32).unsqueeze(0)
        with torch.no_grad():
            logits, value = self.model(state)
        probs = torch.softmax(logits, dim=1).squeeze(0).numpy()
        root.expand(probs)

        # Perform simulations
        for _ in range(self.num_simulations):
            node = root
            path = [node]
            # Selection with dynamic c_puct
            while node.children:
                best_score = -float('inf')
                best_action = None
                for action, child in node.children.items():
                    # Compute UCB with dynamic c_puct
                    ucb = child.Q() + child.dynamic_c_puct * child.prior * math.sqrt(node.visit_count) / (1 + child.visit_count)
                    if ucb > best_score:
                        best_score = ucb
                        best_action = action
                node = node.children[best_action]
                path.append(node)

            # Evaluation of leaf node
            if node.is_terminal:
                leaf_value = node.game.score  # Terminal state value
            else:
                state = torch.tensor(self._state_to_tensor(node.game), dtype=torch.float32).unsqueeze(0)
                with torch.no_grad():
                    logits, value = self.model(state)
                probs = torch.softmax(logits, dim=1).squeeze(0).numpy()
                node.expand(probs)
                leaf_value = value.item()

            # Backpropagate the value
            for n in path:
                n.backpropagate(leaf_value)

        # Select the move with highest visit count
        best_move = None
        best_visit = -1
        for action, child in root.children.items():
            if child.visit_count > best_visit:
                best_visit = child.visit_count
                best_move = action
        return best_move

    def _state_to_tensor(self, game: Game2048):
        """Convert game state to a 16-element tensor (log2 of tiles)."""
        state = []
        for r in range(4):
            for c in range(4):
                val = game.grid[r][c]
                state.append(0 if val == 0 else math.log2(val))
        return state
