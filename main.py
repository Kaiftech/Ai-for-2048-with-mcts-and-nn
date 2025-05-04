# main.py

import tkinter as tk
from game2048 import Game2048
from model import Model
from agent import Agent
from evolution import evolve_agents, save_agents, load_agents
from gui import GameGUI

def main():
    num_agents = 6
    max_moves = 80
    generation = 0
    move_counter = 0

    try:
        agents = load_agents()  # Try to load saved agents
        print("[INFO] Loaded saved agents.")
    except:
        print("[INFO] No saved agents found, creating new ones.")
        agents = [Agent(Model()) for _ in range(num_agents)]  # Initialize new agents if none found

    # Assign initial games to agents
    games = [Game2048() for _ in range(num_agents)]
    for agent, game in zip(agents, games):
        agent.game = game

    # Set up GUI
    gui = GameGUI(agents)

    def simulation_step():
        nonlocal agents, games, move_counter, generation

        for i, agent in enumerate(agents):
            if not agent.game.is_done():  # Check if the game is over
                agent.play_move()  # Use play_move instead of select_move
                # Removed agent.update_score line since score is already updated in Game2048

        move_counter += 1

        if move_counter >= max_moves:  # Reset after a certain number of moves
            move_counter = 0
            generation += 1
            print(f"[INFO] Generation {generation} completed")

            # Log scores
            fitness_scores = [agent.compute_fitness() for agent in agents]  # Use compute_fitness instead of score
            print("[FITNESS SCORES]", fitness_scores)

            # Evolve the agents based on their performance and save them
            agents = evolve_agents(agents, mutation_rate=0.05)
            save_agents(agents)

            # Reset games for the new generation of agents
            games = [Game2048() for _ in range(num_agents)]
            for agent, game in zip(agents, games):
                agent.game = game

        # Update the GUI to reflect the current state of the game
        gui.update_all(agents, generation)
        gui.root.after(20, simulation_step)  # Call the function after 50ms to simulate next step

    # Start the simulation loop
    gui.root.after(20, simulation_step)
    gui.root.mainloop()

if __name__ == "__main__":
    main()
