import torch
import torch.nn as nn
import torch.optim as optim
import os
import numpy as np


class NN(nn.Module):
    def __init__(self, input_size=12, hidden_size=64, output_size=4):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, hidden_size)
        self.linear3 = nn.Linear(hidden_size, output_size)
        self.relu = nn.ReLU()
        self.tanh = nn.Tanh()
        self.soft = nn.Softmax()

    def forward(self, x):
        x = self.linear1(x)
        x = self.relu(x)
        x = self.linear2(x)
        x = self.relu(x)
        x = self.linear3(x)
        x = self.soft(x)
        return x

    def save(self, file_name='model.pth'):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)


class Trainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, old_state, action, reward, target_state, done):
        old_state = torch.tensor(old_state, dtype=torch.float)
        target_state = torch.tensor(target_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        if len(old_state.shape) == 1:
            old_state = torch.unsqueeze(old_state, 0)
            target_state = torch.unsqueeze(target_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        pred = self.model(old_state)

        target = pred.clone()

        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(target_state[idx]))

            target[idx][torch.argmax(action).item()] = Q_new

            # target[0] = torch.tensor(int(np.round(Q_1.detach().numpy())))
            # target[1] = torch.tensor(int(np.round(Q_2.detach().numpy())))
            # target[0] = Q_1
            # target[1] = Q_2

        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()
        self.optimizer.step()
