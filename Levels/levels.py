import pygame


class Levels(object):
    def __init__(self):
        self.block_positions = []

    def draw_level1(self, surface, screen_width, screen_height, gridsize):
        self.block_positions = self.load_level1_blocks(screen_width,
                                                       screen_height, gridsize)
        for block in self.block_positions:
            r = pygame.Rect(block, (gridsize, gridsize))
            pygame.draw.rect(surface, (0, 0, 0), r)

    def draw_level2(self, surface, screen_width, screen_height, gridsize):
        self.block_positions = self.load_level2_blocks(screen_width,
                                                       screen_height, gridsize)
        for block in self.block_positions:
            r = pygame.Rect(block, (gridsize, gridsize))
            pygame.draw.rect(surface, (0, 0, 0), r)

    def load_level1_blocks(self, screen_width, screen_height, gridsize):
        block_list = []
        for tp_block in range(0, screen_width, gridsize):
            block_list.append((tp_block, 0))

        for bt_block in range(0, screen_width, gridsize):
            block_list.append((bt_block, screen_height - gridsize))

        for lft_block in range(0, screen_height, gridsize):
            block_list.append((0, lft_block))

        for rgt_block in range(0, screen_height, gridsize):
            block_list.append((screen_width - gridsize, rgt_block))

        blocks = set(block_list)

        return list(blocks)

    def load_level2_blocks(self, screen_width, screen_height, gridsize):
        block_list = []
        for tp_block in range(5 * gridsize, screen_width - 5 * gridsize,
                              gridsize):
            block_list.append((tp_block, 3 * gridsize))

        for bt_block in range(5 * gridsize, screen_width - 5 * gridsize,
                              gridsize):
            block_list.append((bt_block, screen_height - gridsize - 3 * gridsize))

        for lft_block in range(0, screen_height, gridsize):
            block_list.append((0, lft_block))

        for rgt_block in range(0, screen_height, gridsize):
            block_list.append((screen_width - gridsize, rgt_block))

        blocks = set(block_list)

        return list(blocks)
