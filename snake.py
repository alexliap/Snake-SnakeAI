import pygame
import sys
import random


class Snake(object):
    def __init__(self, screen_width, screen_height, gridsize, grid_width,
                 grid_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        # self.up = (0, -1)
        # self.down = (0, 1)
        # self.left = (-1, 0)
        # self.right = (1, 0)

        self.length = 1
        self.positions = [((self.screen_width / 2), (self.screen_height / 2))]
        self.direction = random.choice([(0, -1), (0, 1), (-1, 0),
                                        (1, 0)])
        self.color = (17, 24, 47)
        self.reseted = False

        self.gridsize = gridsize
        self.grid_width = grid_width
        self.grid_height = grid_height

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x*self.gridsize)) % self.screen_width),
               (cur[1]+(y*self.gridsize)) % self.screen_height)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
            self.reseted = True
        else:
            self.reseted = False
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((self.screen_width/2), (self.screen_height/2))]
        self.direction = random.choice([(0, -1), (0, 1), (-1, 0),
                                        (1, 0)])

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect(p, (self.gridsize, self.gridsize))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (0, 153, 0), r)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn((0, -1))
                elif event.key == pygame.K_DOWN:
                    self.turn((0, 1))
                elif event.key == pygame.K_LEFT:
                    self.turn((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    self.turn((1, 0))
