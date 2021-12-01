import pygame
from snake import Snake
from food import Food
from Levels.levels import Levels


class SnakeGame:
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
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((screen_width, screen_height),
                                              0, 32)
        self.surface = pygame.Surface(self.screen.get_size()).convert()
        self.draw_grid()

        self.snake = Snake(screen_width, screen_height, gridsize,
                           grid_width, grid_height)
        self.food = Food(gridsize, grid_width, grid_height)

        self.levels = Levels()

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

    def reward_punish(self):
        # REWARD
        if self.snake.get_head_position() == self.food.position:
            self.snake.length += 1
            self.score += 1
            self.food.randomize_position()
        # PUNISHMENT
        elif self.snake.get_head_position() in self.levels.block_positions:
            self.snake.reset()
            self.levels.block_positions = []
            self.snake.reseted = True
            self.food.randomize_position()

    def play_step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        self.clock.tick(10)
        self.snake.handle_keys()
        self.draw_grid()
        self.draw_level()
        self.load_food_banned_positions()
        self.snake.move()
        self.reward_punish()
        if self.snake.reseted:
            self.score = 0

        self.snake.draw(self.surface)
        self.food.draw()
        self.screen.blit(self.surface, (0, 0))
        self.food.load_graphic('apple.png', self.screen)

        pygame.display.set_caption('Snake - Current Score {0}'.format(self.score))

        pygame.display.update()

        return self.score

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
    game = SnakeGame(480, 480, 24, 24, 20)

    while True:
        score = game.play_step()
