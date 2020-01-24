#!/usr/bin/env python

import pygame
import random
import sys

from enum import Enum
from collections import defaultdict
        

class BOARD_MANAGER:
    def __init__(self, rows, cols, blockSize):
        self.rows = rows
        self.cols = cols
        self.blockSize = blockSize
        self.width = cols * blockSize
        self.height = rows * blockSize
    
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

class COLOURS:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    GREY = (200, 200, 200)
    ORANGE = (255, 128, 0)
    SKY_BLUE = (135, 206, 235)
    INDIGO = (70, 0, 130)
    YELLOW = (255, 255, 0)    

    @staticmethod
    def GetRandomColour(select=True):
        if not select:
            return (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
        else:
            return random.choice([COLOURS.WHITE, COLOURS.YELLOW, COLOURS.RED, COLOURS.INDIGO, COLOURS.GREEN, COLOURS.ORANGE, COLOURS.SKY_BLUE])

grid_data = defaultdict(lambda: False)
    
def get_square_at(pos):        
    return size_manager.get_row_and_col_from_pos(pos)    
            
def draw_grid(screen):    
    for x in range(size_manager.rows+1):
        pygame.draw.line(screen, COLOURS.WHITE, size_manager.get_pos_by_row_and_col(x,0), size_manager.get_pos_by_row_and_col(x,size_manager.cols), 1)        
        for y in range(size_manager.cols+1):
            pygame.draw.line(screen, COLOURS.WHITE, size_manager.get_pos_by_row_and_col(0,y), size_manager.get_pos_by_row_and_col(size_manager.rows,y), 1)        
               
def draw_text_in_block(text,pos,screen, font_size=11):    
    font = pygame.font.Font("freesansbold.ttf", font_size)    
    t = font.render(text, True, COLOURS.BLACK, COLOURS.WHITE)
    textRect = t.get_rect()
    textRect.center = ((pos[0]+SQUARE_SIZE//2 ), (pos[1] +SQUARE_SIZE//2))
    screen.blit(t, textRect)

def is_valid_placement(r,c):
    for d in range(ROWS):  
        if queens[(r, d)]:            
            return False

        if queens[(d, c)]:
            return False
        
        if ((r - d) >= 0 and (c - d) >= 0 and queens[(r - d, c - d)]) or \
            (r-d >= 0 and (c+d < ROWS) and queens[(r-d, c+d)]):
            return False

        if (r + d < ROWS and c - d >= 0 and queens[(r + d, c - d)]) or \
            (r+d < ROWS and (c+d < ROWS) and queens[(r+d, c+d)]):
            return False
    return True

def solve(col=0):
    if col == ROWS:
        return True
        print("Solved!")        
    for r in range(ROWS):        
        if is_valid_placement(r, col):
            queens[(r, col)] = True                        
            if solve(col+1):
                return True
            queens[(r, col)] = False


solved = False


def solveNonRecursively():
    r = 0
    c = 0
    global solved
    while True and not solved:                        
        if (c + 1 > ROWS):
            print("Solved!")                  
            solved = True                                                
        if is_valid_placement(r, c):
            queens[(r, c)] = True
            yield
            c += 1
            r = 0
        else:            
            queens[(r, c)] = False            
            yield
            r += 1            
            if r+1 > ROWS:
                queens[(r, c - 1)] = False
                c -= 1                
                r = 0                        
                yield                

########################################################################################    
pygame.init()
ROWS = 8
SQUARE_SIZE = 20

size_manager = BOARD_MANAGER(ROWS, ROWS, SQUARE_SIZE)

# Set the width and height of the screen [width, height]
size = (size_manager.width, size_manager.height)

screen = pygame.display.set_mode((size[0]+1, size[1]+1)) 
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# game variables
BUTTON_LEFT = 1
BUTTON_RIGHT = 3

queens = defaultdict(lambda: False)
#solve()
solver = solveNonRecursively() #if you want to view the animation
# -------- Main Program Loop -----------
while not done:    
    # --- Main event loop
    handle_left_click = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            done = True
            continue                                   
        if event.type == pygame.MOUSEBUTTONUP and event.button == BUTTON_LEFT and not handle_left_click:            
            handle_left_click = True
            pos = pygame.mouse.get_pos()   
            clicked_square = size_manager.get_row_and_col_from_pos(pos)            
            clicked_row, clicked_col = size_manager.get_row_and_col_from_pos(pos)            
            if is_valid_placement(clicked_row, clicked_col):
                print("Valid placement!")                                                

    # --- Game logic should go here    
    if not solved:
        try:
            solver.__next__()
        except StopIteration:
            solved=  True
            print("solved")
            pass
    # --- Screen-clearing code goes here          
    screen.fill(COLOURS.BLACK)
 
    # --- Drawing code should go here        (update game visuals / no logic here!)
    # draw a grid    
    draw_grid(screen)
    
    #update grid
    
    for k in grid_data:              
        pos = size_manager.get_pos_by_row_and_col(k[0], k[1])        
        pygame.draw.rect(screen, COLOURS.RED if grid_data[k] else COLOURS.BLACK, [pos[0] + 1, pos[1] + 1, SQUARE_SIZE - 1, SQUARE_SIZE - 1])            
    
    for k in queens:
        if queens[k]:
            pos = size_manager.get_pos_by_row_and_col(k[0], k[1])
            pygame.draw.circle(screen, COLOURS.GREEN, [pos[0] + SQUARE_SIZE // 2, pos[1] + SQUARE_SIZE // 2], SQUARE_SIZE // 4)        
    
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to x frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()