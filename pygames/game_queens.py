#!/usr/bin/env python

import pygame
import random
import sys

from enum import Enum
from collections import defaultdict
class TILE_TYPE(Enum):    
    VISIBLE = 1
    COLLAPSABLE = 2
    COLLAPSED = 4
    OUTLINED = 8

class SQUARE_DATA:    
    def __init__(self, t, label="P"):        
        self.Square_Type = t
        self.Label = label
        d = random.random()        
        if d < 0.2:
            self.Colour = COLOURS.RED
        else:
            self.Colour = COLOURS.GetRandomColour()
    def __repr__(self):
        return f"Square Type: {self.Square_Type} Color: {self.Colour}"
        
class Position:
    def __init__(self, width, height):
        self.width = width
        self.height = height
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


class Game:
    run = True
    def __init__(self):
        pass
    def run(self):
        while run:
            pass

NUMBER_OF_SQUARES_TO_UNCOVER = 1

grid_data = {}
def has_top(clicked_square):
    #check row
    return (clicked_square[0] >= 1) 

def has_bottom(clicked_square):
    return (clicked_square[0] < size_manager.rows-1)

def has_left(clicked_square):
    return (clicked_square[1] > 0)
    
def has_right(clicked_square):
    return (clicked_square[1] < size_manager.cols-1)
    
def process_blocks(clicked_square, target_color):        
    if grid_data[clicked_square].Square_Type in [TILE_TYPE.COLLAPSED, TILE_TYPE.COLLAPSABLE, TILE_TYPE.OUTLINED]:
        return
    
    if grid_data[clicked_square].Colour == target_color:                        
        neighbouring_squares = get_neighbouring_cross(clicked_square)
        grid_data[clicked_square].Square_Type = TILE_TYPE.OUTLINED
        for square in neighbouring_squares:        
            process_blocks(square, target_color)

def apply_collapsed(size, rows, cols):    
    move_left = False
    for col in range(0, cols): 
        blocks = [b for b in get_blocks_by_col(col) if grid_data[b].Square_Type == TILE_TYPE.OUTLINED]        
        #collapse this column
        
        for b in blocks:              
            move_block_down(b)  #works brilliantly
    
    for col in range(cols):
        if does_col_need_left_shift(col):            
            move_col_left(col)

def move_block_down(square):
    if grid_data[square].Square_Type == TILE_TYPE.COLLAPSED:
        return

    if not has_top(square):
        grid_data[square].Colour = COLOURS.BLACK
        grid_data[square].Square_Type = TILE_TYPE.COLLAPSED
        return    

    top = (square[0]-1, square[1])
    
    grid_data[square].Colour = grid_data[top].Colour
    grid_data[square].Label = grid_data[top].Label
    grid_data[square].Square_Type = TILE_TYPE.VISIBLE
    
    move_block_down(top)

def does_col_need_left_shift(col):
    blocks = get_blocks_by_col(col)    
    return len(blocks) == len([b for b in blocks if grid_data[b].Colour == COLOURS.BLACK])
    
def move_col_left(col):    
    for r in range(size_manager.rows):        
        if not has_right((r,col)):
            grid_data[(r,col)].Colour = COLOURS.BLACK
            grid_data[(r,col)].Square_Type = TILE_TYPE.VISIBLE                
        else:            
            grid_data[(r, col)].Colour = grid_data[(r, col + 1)].Colour
            grid_data[(r,col)].Label = grid_data[(r,col+1)].Label
            grid_data[(r,col)].Square_Type = TILE_TYPE.VISIBLE            
            
            grid_data[(r,col+1)].Colour = COLOURS.BLACK
            grid_data[(r,col+1)].Square_Type = TILE_TYPE.VISIBLE
   
def get_blocks_by_col(col):    
    if col-1 > size_manager.cols or col < 0:
        return []    
    blocks = []
    for r in range(size_manager.rows):
        blocks.append((r,col))    
    return blocks

def get_neighbouring_cross(square):    
    squares = []
    if has_top(square):
        squares.append((square[0]-1,square[1])) #T        
    if has_bottom(square):
        squares.append((square[0]+1, square[1])) #B        
    if has_right(square):
        squares.append((square[0], square[1]+1))  #R
    if has_left(square):
        squares.append((square[0],square[1]-1))  #L    
    return squares

    
def get_square_at(pos):        
    return size_manager.get_row_and_col_from_pos(pos)    
            
def draw_grid(screen):    
    for x in range(size_manager.rows):
        pygame.draw.line(screen, COLOURS.WHITE, size_manager.get_pos_by_row_and_col(x,0), size_manager.get_pos_by_row_and_col(x,size_manager.cols), 1)        
        for y in range(size_manager.cols):
            pygame.draw.line(screen, COLOURS.WHITE, size_manager.get_pos_by_row_and_col(0,y), size_manager.get_pos_by_row_and_col(size_manager.rows,y), 1)        
               
def draw_text_in_block(text,pos,screen, font_size=11):    
    font = pygame.font.Font("freesansbold.ttf", font_size)    
    t = font.render(text, True, COLOURS.BLACK, COLOURS.WHITE)
    textRect = t.get_rect()
    textRect.center = ((pos[0]+SQUARE_SIZE//2 ), (pos[1] +SQUARE_SIZE//2))
    screen.blit(t, textRect)
    
def create_level(size):    
    for col in range(COLS):        
        for row in range(ROWS):
            grid_data[(row,col)] = SQUARE_DATA(TILE_TYPE.VISIBLE)              
            grid_data[(row, col)].Square_Type = TILE_TYPE.VISIBLE
            grid_data[(row,col)].Label = f"{row}:{col}"

def update_score():
    s = f"SAME GAME{1}"
    pygame.display.set_caption("SAME GAME")
########################################################################################    
pygame.init()
ROWS = 5
COLS = 5
SQUARE_SIZE = 100

size_manager = BOARD_MANAGER(ROWS, COLS, SQUARE_SIZE)

# Set the width and height of the screen [width, height]
size = (size_manager.width, size_manager.height)

screen = pygame.display.set_mode((size[0], size[1])) 
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# game variables
BUTTON_LEFT = 1
BUTTON_RIGHT = 3

pos = (0, 0)
clicked_square = (0, 0)
selected_squares = []

create_level(size) #fill with mines
print(f"rows: {ROWS} cols: {COLS}")
                               
# -------- Main Program Loop -----------
#Game().run()
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
            if grid_data[clicked_square].Square_Type == TILE_TYPE.OUTLINED: #the user has clicked an outlined block                
                apply_collapsed(size, ROWS, COLS)                
                continue
                        
            for k in [m for m in grid_data if grid_data[m].Square_Type == TILE_TYPE.OUTLINED]:
                grid_data[k].Square_Type = TILE_TYPE.VISIBLE            
            
            process_blocks(clicked_square, grid_data[clicked_square].Colour)  #the game runs inside this                                    
            
            #update_score()

    # --- Game logic should go here
    
    # --- Screen-clearing code goes here          
    screen.fill(COLOURS.BLACK)
 
    # --- Drawing code should go here        (update game visuals / no logic here!)
    # draw a grid    
    draw_grid(screen)
    
    #update grid
    
    for k in grid_data:              
        pos = size_manager.get_pos_by_row_and_col(k[0], k[1])        
        pygame.draw.rect(screen, grid_data[k].Colour, [pos[0]+1 , pos[1]+1, SQUARE_SIZE-1 , SQUARE_SIZE-1])
    
    for k in [m for m in grid_data if grid_data[m].Square_Type == TILE_TYPE.OUTLINED]:
        marker_size = SQUARE_SIZE // 2
        pos = size_manager.get_pos_by_row_and_col(k[0], k[1])
        pygame.draw.rect(screen, COLOURS.BLACK, [pos[0] + marker_size // 2, pos[1] + marker_size // 2, marker_size, marker_size])
    
    #for k in grid_data:
    #    draw_text_in_block(grid_data[k].Label, (k[1] * SQUARE_SIZE,k[0]*SQUARE_SIZE), screen)
            
    
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to x frames per second
    clock.tick(10)
 
# Close the window and quit.
pygame.quit()