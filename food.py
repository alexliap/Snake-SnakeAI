import pygame
import random


class Food(object):
    """
    Food obnject of the game.

    Args:
        grid_width: int
            Number of game blocks along the X axis.

        grid_height: int
            Number of game blocks along the Y axis.

        gridsize: int
            X and Y dimension of the game blocks.
    """
    def __init__(self, gridsize, grid_width, grid_height):
        self.position = (0, 0)
        self.banned_positions = []
        self.color = (223, 163, 49)

        self.gridsize = gridsize
        self.grid_width = grid_width
        self.grid_height = grid_height

        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, self.grid_width - 1) * self.gridsize,
                         random.randint(0, self.grid_height - 1) * self.gridsize)
        while self.position in self.banned_positions:
            self.position = (random.randint(0, self.grid_width - 1) * self.gridsize,
                             random.randint(0, self.grid_height - 1) * self.gridsize)

    def draw(self):
        pygame.Rect((self.position[0], self.position[1]),
                    (self.gridsize, self.gridsize))

        # This line is for drawing rectangle apples.
        # pygame.draw.rect(surface, self.color, r)

    def load_graphic(self, image, screen):
        apple = pygame.image.load(image)
        screen.blit(apple, self.position)
