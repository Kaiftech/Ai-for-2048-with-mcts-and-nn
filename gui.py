# gui.py

import tkinter as tk

class GameGUI:
    def __init__(self, agents):
        self.agents = agents
        self.root = tk.Tk()
        self.root.title("2048 AI Arena")
        # Generation label
        self.gen_label = tk.Label(self.root, text="Gen: 0", font=("Arial", 16))
        self.gen_label.grid(row=0, column=0, columnspan=3, pady=10)
        # Create frames for 6 boards
        self.board_labels = []   # list of 6 boards, each a 4x4 list of Labels
        self.score_labels = []   # list of 6 score Labels
        for i in range(6):
            frame = tk.Frame(self.root, relief=tk.RAISED, bd=2)
            row = 1 + i // 3
            col = i % 3
            frame.grid(row=row, column=col, padx=5, pady=5)
            board_grid = []
            for r in range(4):
                row_labels = []
                for c in range(4):
                    lbl = tk.Label(frame, text="", width=4, height=2, font=("Arial", 14),
                                   borderwidth=1, relief="solid")
                    lbl.grid(row=r, column=c, padx=2, pady=2)
                    row_labels.append(lbl)
                board_grid.append(row_labels)
            # Score label below each board
            score_lbl = tk.Label(frame, text="Score: 0", font=("Arial", 12))
            score_lbl.grid(row=4, column=0, columnspan=4, pady=5)
            self.board_labels.append(board_grid)
            self.score_labels.append(score_lbl)

    def update_agent(self, idx, agent):
        """Update the board and score for one agent."""
        # Update tiles
        grid = agent.game.grid
        for r in range(4):
            for c in range(4):
                val = grid[r][c]
                text = str(val) if val != 0 else ""
                self.board_labels[idx][r][c].config(text=text)
        # Update score
        self.score_labels[idx].config(text=f"Score: {agent.score}")

    def update_all(self, agents, generation):
        """Update all boards and the generation label."""
        self.gen_label.config(text=f"Gen: {generation}")
        for idx, agent in enumerate(agents):
            self.update_agent(idx, agent)

    def update_generation(self, generation):
        """Update the generation label only."""
        self.gen_label.config(text=f"Gen: {generation}")
