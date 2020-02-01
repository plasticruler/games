import pygame
from utils import COLOURS



class BOARD_MANAGER:
    def __init__(self, rows, cols, blockSize=25):
        self.rows = rows
        self.cols = cols
        self.blockSize = blockSize
        self.width = cols * blockSize
        self.height = rows * blockSize
        self.size = (self.width, self.height)
        self.screen = pygame.display.set_mode((self.size[0] + 1, self.size[1] + 1))

    def get_pos_by_row_and_col(self, row, col):
        if col-1 > self.cols:
            raise ValueError("Invalid column referenced.")
        if row-1 > self.rows:
            raise ValueError("Invalid row referenced.")
        return (col * self.blockSize, row * self.blockSize)

    def get_row_and_col_from_pos(self, pos):
        return ((pos[1] // self.blockSize), (pos[0] // self.blockSize))

    def is_row_valid(self, row):
        return row < self.rows

    def get_square_at(self, pos):
        return self.get_row_and_col_from_pos(pos)

    def draw_grid(self):
        for x in range(self.rows+1):
            pygame.draw.line(self.screen, COLOURS.WHITE, self.get_pos_by_row_and_col(
                x, 0), self.get_pos_by_row_and_col(x, self.cols), 1)
            for y in range(self.cols+1):
                pygame.draw.line(self.screen, COLOURS.WHITE, self.get_pos_by_row_and_col(
                    0, y), self.get_pos_by_row_and_col(self.rows, y), 1)

    def draw_text_in_block(self, text, pos, font_size=11):
        font = pygame.font.Font("freesansbold.ttf", font_size)
        t = font.render(text, True, COLOURS.BLACK, COLOURS.WHITE)
        textRect = t.get_rect()
        textRect.center = ((pos[0] + self.blockSize // 2),
                        (pos[1] + self.blockSize // 2))
        self.screen.blit(t, textRect)