import torch
import torch.nn as nn

class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.fc1 = nn.Linear(16, 64)
        self.relu = nn.ReLU()
        self.fc_policy = nn.Linear(64, 4)  # Up, Down, Left, Right
        self.fc_value = nn.Linear(64, 1)

    def forward(self, x):
        x = self.relu(self.fc1(x))
        policy = self.fc_policy(x)
        value = self.fc_value(x)
        return policy, value

    def save(self, path):
        torch.save(self.state_dict(), path)

    def load(self, path):
        self.load_state_dict(torch.load(path))
        self.eval()  # Evaluation mode (disable dropout etc.)
