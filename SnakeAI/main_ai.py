import pygame
import numpy as np
from snake_ai import Snake
from food import Food
from Levels.levels import Levels


class SnakeGameAI:
    def __init__(self, screen_width, screen_height, grid_width,
                 grid_height, gridsize):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.gridsize = gridsize
        pygame.init()
        pygame.display.set_caption('Snake')
        icon = pygame.image.load('anaconda.png')
        pygame.display.set_icon(icon)
        self.score = 0
        self.frame_iteration = 0
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((screen_width, screen_height),
                                              0, 32)
        self.surface = pygame.Surface(self.screen.get_size()).convert()
        self.draw_grid()

        self.snake = Snake(screen_width, screen_height, gridsize,
                           grid_width, grid_height)
        self.food = Food(gridsize, grid_width, grid_height)

        self.levels = Levels()

        self.reward_ai = 0

    def draw_grid(self):
        for y in range(0, int(self.grid_height)):
            for x in range(0, int(self.grid_width)):
                if (x + y) % 2 == 0:
                    r = pygame.Rect((x * self.gridsize, y * self.gridsize),
                                    (self.gridsize, self.gridsize))
                    pygame.draw.rect(self.surface, (93, 216, 218), r)
                else:
                    rr = pygame.Rect((x * self.gridsize, y * self.gridsize),
                                     (self.gridsize, self.gridsize))
                    pygame.draw.rect(self.surface, (84, 194, 205), rr)

    # Distance from Snake's head to Food
    def state(self):
        snake_pos = self.snake.get_head_position()
        food_pos = self.food.position
        x_cord = snake_pos[0]-food_pos[0]
        y_cord = snake_pos[1]-food_pos[1]
        return np.sqrt(x_cord**2 + y_cord**2)

    def find_optimal_turn(self):
        states = []
        cur = self.snake.get_head_position()
        available_turns = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for turn in available_turns:
            x, y = turn
            new = (((cur[0] + (x * self.gridsize)) % self.screen_width),
                   (cur[1] + (y * self.gridsize)) % self.screen_height)
            if len(self.snake.positions) > 2 and new in self.snake.positions[2:]:
                pass
            else:
                # self.snake.positions.insert(0, new)
                food_pos = self.food.position
                x_cord = new[0] - food_pos[0]
                y_cord = new[1] - food_pos[1]
                states.append(np.sqrt(x_cord**2 + y_cord**2))

        optimal_turn = available_turns[states.index(np.min(states))]
        return optimal_turn
        # return available_turns[states.index(np.min(states))]
        # return np.min(states)

    def find_optimal_state_list(self):
        optimal_turn = self.find_optimal_turn()
        x, y = optimal_turn
        cur = self.snake.get_head_position()
        new = (((cur[0] + (x * self.gridsize)) % self.screen_width),
               (cur[1] + (y * self.gridsize)) % self.screen_height)
        optimal_state = self.get_state_list(new, optimal_turn)
        return optimal_state

    def get_state_list(self, snake_head=None, snake_dir=None):
        head = snake_head
        direction = snake_dir
        food = self.food.position
        if (snake_head == None) and (snake_dir == None):
            head = self.snake.get_head_position()
            direction = self.snake.direction
            # food = self.food.position

        point_l = (head[0] - self.gridsize, head[0])
        point_r = (head[0] + self.gridsize, head[0])
        point_u = (head[1], head[1] - self.gridsize)
        point_d = (head[1], head[1] + self.gridsize)

        dir_l = direction == (-1, 0)
        dir_r = direction == (1, 0)
        dir_u = direction == (0, -1)
        dir_d = direction == (0, 1)

        state = [
            # Danger
            (dir_l and point_l in self.levels.block_positions),
            (dir_r and point_r in self.levels.block_positions),
            (dir_u and point_u in self.levels.block_positions),
            (dir_d and point_d in self.levels.block_positions),

            # Direction
            dir_l, dir_r, dir_u, dir_d,
            # Food Location
            head[0] > food[0],
            head[0] < food[0],
            head[1] > food[1],
            head[1] < food[1]
        ]
        return np.array(state, dtype=int)

    def reward_punish(self):
        # REWARD
        if self.snake.get_head_position() == self.food.position:
            self.snake.length += 1
            self.score += 1
            self.food.randomize_position()
            self.reward_ai = 10
        # PUNISHMENT
        elif self.snake.get_head_position() in self.levels.block_positions or \
                self.frame_iteration > 150*self.snake.length:
            self.snake.reset()
            self.levels.block_positions = []
            self.snake.reseted = True
            self.food.randomize_position()
            # self.score = 0
            # self.frame_iteration = 0
            # self.reward_ai = -10

    def play_step(self, action=None):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        total_score = self.score
        self.clock.tick(30)
        self.snake.handle_action(action)
        self.draw_grid()
        self.draw_level()
        self.load_food_banned_positions()
        self.snake.move()
        self.reward_punish()
        if self.snake.reseted:
            self.score = 0
            self.frame_iteration = 0
            self.reward_ai = -10

        self.snake.draw(self.surface)
        self.food.draw()
        self.screen.blit(self.surface, (0, 0))
        self.food.load_graphic('apple.png', self.screen)

        pygame.display.set_caption('Snake - Current Score {0}'.format(self.score))

        pygame.display.update()
        self.frame_iteration += 1

        return self.reward_ai, total_score, self.snake.reseted

    def load_food_banned_positions(self):
        self.food.banned_positions = [*self.levels.block_positions,
                                      *self.snake.positions]
        if self.score >= 8:
            spots = self.levels.load_level2_blocks(self.screen_width,
                                                   self.screen_height,
                                                   self.gridsize)
            self.food.banned_positions = [*spots, *self.snake.positions]

        elif self.score >= 3:
            spots = self.levels.load_level1_blocks(self.screen_width,
                                                   self.screen_height,
                                                   self.gridsize)
            self.food.banned_positions = [*spots, *self.snake.positions]

    def draw_level(self):
        if self.score >= 10:
            self.levels.draw_level2(self.surface, self.screen_width,
                                    self.screen_height, self.gridsize)
        elif self.score >= 5:
            self.levels.draw_level1(self.surface, self.screen_width,
                                    self.screen_height, self.gridsize)


if __name__ == '__main__':
    game = SnakeGameAI(480, 480, 24, 24, 20)

    while True:
        reward, score, game_over = game.play_step()
