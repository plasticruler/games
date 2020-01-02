#!/usr/bin/env python

import pygame
import random
import sys

from enum import Enum
from collections import defaultdict
class TILE_TYPE(Enum):    
    VISIBLE = 1
    COLLAPSED = 2

class SQUARE_DATA:    
    def __init__(self, t, m=0):        
        self.Square_Type = t
        self.Colour = COLOURS.GetRandomColour()


class BLOCK:
    def __init__(pos, d):
        self.pos = pos
        self.data = d
        self.is_obstacle = True


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
            return random.choice([COLOURS.INDIGO, COLOURS.RED, COLOURS.WHITE, COLOURS.GREEN, COLOURS.ORANGE, COLOURS.SKY_BLUE, COLOURS.YELLOW])

NUMBER_OF_SQUARES_TO_UNCOVER = 1

grid_data = defaultdict(lambda:SQUARE_DATA(TILE_TYPE.VISIBLE))

def has_top(pos, size, steps=10):
    return not (pos[1] == 0)
def has_bottom(pos, size, steps=10):
    return not (pos[1] + steps >= size[1])
def has_left(pos, size, steps=10):
    return not (pos[0] == 0 or pos[0]+1 - (steps) <= 0)
def has_right(pos, size, steps=10):
    return not (pos[0] + steps >= size[1])

def process_blocks(pos, size, target_color, steps=10):
    """basically this is just a flood fill"""    
    block_at_pos = grid_data[pos]
    
    if block_at_pos.Square_Type == TILE_TYPE.COLLAPSED:        
        return

    if block_at_pos.Colour == target_color:        
        grid_data[pos].Square_Type = TILE_TYPE.COLLAPSED
        grid_data[pos].Colour = COLOURS.BLACK
    else:
        return
    neighbouring_squares = get_neighbouring_cross(pos, size, steps)
    for square in neighbouring_squares:        
        process_blocks(square, size,target_color, steps)

def get_neighbouring_cross(pos, size, steps=10):
    pos = get_square_at(pos, size, steps)
    squares = []
    if has_top(pos, size, steps):
        squares.append(get_square_at((pos[0], pos[1]-steps), size,steps)) #T        
    if has_bottom(pos, size, steps):
        squares.append(get_square_at((pos[0], pos[1]+steps), size, steps)) #B        
    if has_right(pos, size, steps):
        squares.append(get_square_at((pos[0] + steps, pos[1]), size, steps))  #R
    if has_left(pos, size, steps):
        squares.append(get_square_at((pos[0] - steps, pos[1]), size, steps))  #L
    return squares

def get_neighbouring_squares(pos, size, steps=10):
    pos = get_square_at(pos, size, steps)
    #T,TR,R,BR,B,BL,L,TL
    squares = []
    if has_top(pos, size, steps):
        squares.append(get_square_at((pos[0], pos[1]-steps), size,steps)) #T
        if has_left(pos, size, steps):
            squares.append(get_square_at((pos[0] - steps, pos[1] - steps),size, steps))  #TL
        if has_right(pos, size, steps):
            squares.append(get_square_at((pos[0] + steps, pos[1] - steps), size, steps))  #TR
    if has_bottom(pos, size, steps):
        squares.append(get_square_at((pos[0], pos[1]+steps), size, steps)) #B
        if has_left(pos, size, steps):
            squares.append(get_square_at((pos[0] - steps, pos[1] + steps), size, steps))  #BL
        if has_right(pos, size, steps):
            squares.append(get_square_at((pos[0] + steps, pos[1] + steps),size, steps))  #BR
    if has_right(pos, size, steps):
        squares.append(get_square_at((pos[0] + steps, pos[1]), size, steps))  #R
    if has_left(pos, size, steps):
        squares.append(get_square_at((pos[0] - steps, pos[1]), size, steps))  #L
    return squares
    
def get_square_at(pos, size, steps=10):    
    x = (pos[0] // steps) * steps
    y = (pos[1] // steps) * steps
    return (x,y)
            
def draw_grid(screen, size, steps=10):    
    for x in range(0, size[0] + 1, steps):
        pygame.draw.line(screen, COLOURS.WHITE, (x, 0), (x, size[1]), 1)        
        for y in range(0,size[1]+1, steps):
            pygame.draw.line(screen, COLOURS.WHITE, (0, y), (size[0], y), 1)            
    
            
               
def draw_text_in_block(text, x,y,screen, size,font_size=8, steps=10):
    pos = get_square_at((x, y), size, steps)    
    font = pygame.font.Font("freesansbold.ttf", font_size)
    t = font.render(text, True, COLOURS.BLACK, COLOURS.GREEN)
    textRect = t.get_rect()
    textRect.center = ((pos[0]+steps//2 ), (pos[1] +steps//2))
    screen.blit(t, textRect)
    
def create_level(size, grid_data, steps=10):
    return
    for i in range(size[0] / steps):
        block_colour = COLOURS.GetRandomColour()

    #block_width = size[1] / 
    
pygame.init()
 
# Set the width and height of the screen [width, height]
size = (600, 600)
screen = pygame.display.set_mode((size[0]+2, size[1]+2))
 
pygame.display.set_caption("Minesweeper")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# game variables
BUTTON_LEFT = 1
BUTTON_RIGHT = 3
SQUARE_SIZE = 20
pos = (0, 0)
clicked_square = (0, 0)
selected_squares = []


for x in range(0, size[0] + 1, SQUARE_SIZE):        
        for y in range(0,size[1]+1, SQUARE_SIZE):
            s = get_square_at((x, y), size, SQUARE_SIZE)
            grid_data[s].Square_Type = TILE_TYPE.VISIBLE

create_level(size, grid_data, SQUARE_SIZE) #fill with mines
print("rows: ", int(size[1]/SQUARE_SIZE), " cols: ", int(size[0]/SQUARE_SIZE))
                               
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    handle_left_click = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            done = True
            continue
        if event.type == pygame.MOUSEBUTTONUP and event.button == BUTTON_LEFT and not handle_left_click:                        
            pos = pygame.mouse.get_pos()            
            clicked_square = get_square_at(pos, size, SQUARE_SIZE)            
            process_blocks(clicked_square, size, grid_data[clicked_square].Colour, SQUARE_SIZE) #the game runs inside this
            handle_left_click = True
 
    # --- Game logic should go here
    
    # --- Screen-clearing code goes here          
    screen.fill(COLOURS.BLACK)
 
    # --- Drawing code should go here        (update game visuals / no logic here!)
    # draw a grid    
    draw_grid(screen, size, SQUARE_SIZE)
    
    #update grid
    for k in grid_data:
        pygame.draw.rect(screen, grid_data[k].Colour, [k[0] + 1, k[1] + 1, SQUARE_SIZE - 1, SQUARE_SIZE - 1])
        
    #print labels
    #uncovered_squares = [x for x in grid_data if not (grid_data[x].Square_Type in [TILE_TYPE.MINED_UNCOVERED, TILE_TYPE.MINED, TILE_TYPE.COVERED])]
    #for us in uncovered_squares:                
    #    draw_text_in_block(str(grid_data[us].MineCount),us[0]+1,us[1]+1,screen,size,8,SQUARE_SIZE)                            
    
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to x frames per second
    clock.tick(10)
 
# Close the window and quit.
pygame.quit()