#!/usr/bin/env python

import pygame
import random
import sys

from enum import Enum
from collections import defaultdict
class TILE_TYPE(Enum):    
    MINED = 1
    MINED_UNCOVERED = 2 
    EXPLORED = 3
    COVERED = 4
    UNCOVERED = 5

class SQUARE_DATA:    
    def __init__(self, t, m=0):
        self.MineCount = m
        self.Square_Type = t

class COLOURS:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    GREY = (200,200,200)


NUMBER_OF_SQUARES_TO_UNCOVER = 5

grid_data = defaultdict(lambda:SQUARE_DATA(TILE_TYPE.COVERED))

def has_top(pos, size, steps=10):
    return not (pos[1] == 0)
def has_bottom(pos, size, steps=10):
    return not (pos[1] + steps >= size[1])
def has_left(pos, size, steps=10):
    return not (pos[0] == 0 or pos[0]+1 - (steps) <= 0)
def has_right(pos, size, steps=10):
    return not (pos[0] + steps >= size[1])

def flood_fill(pos, size, steps=10, n=NUMBER_OF_SQUARES_TO_UNCOVER):
    """basically this is just a flood fill"""
    if n <= 0:
        return

    if grid_data[pos].Square_Type in [TILE_TYPE.UNCOVERED, TILE_TYPE.MINED_UNCOVERED]:        
        return    

    if grid_data[pos].Square_Type == TILE_TYPE.MINED:
        grid_data[pos].Square_Type = TILE_TYPE.MINED_UNCOVERED
    else:
        grid_data[pos].Square_Type = TILE_TYPE.UNCOVERED
    
    neighbouring_squares = get_neighbouring_cross(pos, size, steps)
    for square in neighbouring_squares:        
        flood_fill(square, size, steps, n-1)

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
    
def random_fill(size, grid_data, steps=10):    
    for i in range(SQUARE_SIZE * SQUARE_SIZE):
        x = random.randint(0, size[0])
        y = random.randrange(0, size[1])
        p = get_square_at((x, y), size, steps)
        grid_data[p] = SQUARE_DATA(TILE_TYPE.MINED)    
    
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
            grid_data[s].Square_Type = TILE_TYPE.COVERED

random_fill(size, grid_data, SQUARE_SIZE) #fill with mines

#at game start all tiles are covered or mined, get all covered tiles and update
#the surrounding minecount
covered_squares = [x for x in grid_data if grid_data[x].Square_Type == TILE_TYPE.COVERED]
for us in covered_squares:
    surrounding_blocks = get_neighbouring_squares((us[0], us[1]), size, SQUARE_SIZE)
    for b in surrounding_blocks:
        if grid_data[b].Square_Type == TILE_TYPE.MINED:
            grid_data[us].MineCount += 1            
                               
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
            flood_fill(clicked_square, size, SQUARE_SIZE)
            if grid_data[clicked_square].Square_Type == TILE_TYPE.MINED_UNCOVERED:
                print("You died!")
                sys.exit(1)            
            handle_left_click = True
 
    # --- Game logic should go here
    covered_squares = [x for x in grid_data if (grid_data[x].Square_Type in [TILE_TYPE.COVERED])]
    if len(covered_squares) == 0:
        print("You won!")
        sys.exit(0)
    

    # --- Screen-clearing code goes here          
    screen.fill(COLOURS.BLACK)
 
    # --- Drawing code should go here        (update game visuals / no logic here!)
    # draw a grid    
    draw_grid(screen, size, SQUARE_SIZE)
    if handle_left_click:        
        handle_left_click = False
    #update grid
    for k in grid_data:
        if grid_data[k].Square_Type == TILE_TYPE.UNCOVERED: #fill grid
            pygame.draw.rect(screen, COLOURS.GREEN, [k[0] + 1, k[1] + 1, SQUARE_SIZE - 1, SQUARE_SIZE - 1])

        if grid_data[k].Square_Type == TILE_TYPE.MINED_UNCOVERED:
            pygame.draw.rect(screen, COLOURS.RED, [k[0] + 1, k[1] + 1, SQUARE_SIZE - 1, SQUARE_SIZE - 1])                

    #print labels
    uncovered_squares = [x for x in grid_data if not (grid_data[x].Square_Type in [TILE_TYPE.MINED_UNCOVERED, TILE_TYPE.MINED, TILE_TYPE.COVERED])]
    for us in uncovered_squares:                
        draw_text_in_block(str(grid_data[us].MineCount),us[0]+1,us[1]+1,screen,size,8,SQUARE_SIZE)                            
    
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to x frames per second
    clock.tick(10)
 
# Close the window and quit.
pygame.quit()