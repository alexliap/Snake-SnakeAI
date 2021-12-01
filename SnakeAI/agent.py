import torch
import random
import numpy as np
from collections import deque
from main_ai import SnakeGameAI
from model import Trainer, NN
from helper import plot


MAX_MEMORY = 100000
BATCH_SIZE = 1000
LR = 0.01


class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = NN()
        self.trainer = Trainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        return game.get_state_list()

    def remember(self, state, action, reward, target_state, done):
        self.memory.append((state, action, reward, target_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # LIST OF TUPLES
        else:
            mini_sample = self.memory

        # states, actions, rewards, next_states, dones = zip(*mini_sample)
        # self.trainer.train_step(states, actions, rewards, next_states, dones)
        # OR
        for state, action, reward, target_state, done in mini_sample:
            self.trainer.train_step(state, action, reward, target_state, done)

    def train_short_memory(self, state, action, reward, target_state, done):
        self.trainer.train_step(state, action, reward, target_state, done)

    def action(self, state):
        self.epsilon = 30 - self.n_games
        available_actions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        if random.randint(0, 30) < self.epsilon:
            return random.choice(available_actions)
        else:
            state = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state)
            move = np.array((0, 0, 0, 0))
            move[torch.argmax(prediction)] = 1  # prediction[torch.argmax(prediction)].numpy()
            action = self.move_to_action(move)
            return action

    def move_to_action(self, move):
        if move[0] == 1:
            return 0, -1
        elif move[1] == 1:
            return 0, 1
        elif move[2] == 1:
            return -1, 0
        elif move[3] == 1:
            return 1, 0


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI(480, 480, 24, 24, 20)
    while True:
        old_state = agent.get_state(game)
        final_move = agent.action(old_state)
        reward, score, game_over = game.play_step(final_move)
        # new_state = agent.get_state(game)
        target_state = game.find_optimal_state_list()
        # target_state = agent.get_state(game)

        agent.train_short_memory(old_state, final_move, reward, target_state, game_over)
        agent.remember(old_state, final_move, reward, target_state, game_over)

        if game_over:
            agent.train_long_memory()
            agent.n_games += 1

            if score > record:
                record = score
            #     agent.model.save()

            print('Game', agent.n_games, 'Score:', score, 'Record:', record)

            # plot_scores.append(score)
            # total_score += score
            # mean_score = total_score / agent.n_games
            # plot_mean_scores.append(mean_score)
            # plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    train()
