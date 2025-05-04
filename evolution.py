# evolution.py

import copy
import torch
import os
import pickle
from agent import Agent
from model import Model

def evolve_agents(agents, mutation_rate=0.02):
    """
    Perform selection and mutation:
    - Sort agents by fitness (descending).
    - Top 3 survive as-is.
    - Bottom 3 are replaced by mutated clones of the top 3.
    """
    # Sort agents by fitness (high to low) based on the new fitness function
    sorted_agents = sorted(agents, key=lambda a: a.compute_fitness(), reverse=True)
    top3 = sorted_agents[:3]
    new_agents = []
    # Keep top 3
    for agent in top3:
        new_agents.append(agent)
    # Replace bottom 3 with mutated copies of top 3
    for i in range(3):
        parent = top3[i]
        # Deepcopy the parent's model parameters
        child_model = Model()
        child_model.load_state_dict(parent.model.state_dict())
        # Mutate weights: add Gaussian noise
        for param in child_model.parameters():
            noise = torch.randn_like(param) * mutation_rate
            param.data.add_(noise)
        # Create new Agent with this mutated model
        new_agent = Agent(model=child_model)
        new_agents.append(new_agent)
    return new_agents


def save_agents(agents, filename="agents.pkl"):
    """
    Save agents to a file using pickle.
    """
    with open(filename, 'wb') as f:
        pickle.dump(agents, f)
    print(f"[INFO] Saved agents to {filename}")


def load_agents(filename="agents.pkl"):
    """
    Load agents from a file using pickle.
    If no saved agents are found, initialize new ones.
    """
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            agents = pickle.load(f)
        print(f"[INFO] Loaded agents from {filename}")
    else:
        print(f"[INFO] No saved agents found, creating new ones.")
        agents = initialize_agents()  # Function to initialize new agents
    return agents

def initialize_agents(num_agents=6):
    """
    Initialize a set of new agents.
    """
    agents = []
    for _ in range(num_agents):
        model = Model()  # Create a new model for each agent
        agent = Agent(model=model)  # Create a new agent
        agents.append(agent)
    return agents
