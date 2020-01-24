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
    def __init__(self, t, m=0):        
        self.Square_Type = t        
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
        return (pos[1] // self.blockSize, pos[0] // self.blockSize)
    
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
            return random.choice([COLOURS.RED, COLOURS.GREY, COLOURS.INDIGO, COLOURS.WHITE, COLOURS.GREEN, COLOURS.ORANGE, COLOURS.SKY_BLUE, COLOURS.YELLOW])


class Game:
    run = True
    def __init__(self):
        pass
    def run(self):
        while run:
            pass

NUMBER_OF_SQUARES_TO_UNCOVER = 1

grid_data = defaultdict(lambda:SQUARE_DATA(TILE_TYPE.VISIBLE))

def has_top(pos, size):
    return not (pos[1] == 0)

def has_bottom(pos, size, steps=10):
    return not (pos[1] + steps >= size[1])

def has_left(pos, size, steps=10):
    return not (pos[0] == 0 or pos[0] + 1 - (steps) <= 0)
    
def has_right(pos, size, steps=10):
    return (pos[0] + steps < size[0])
    
def process_blocks(pos, size, target_color, steps=10):        
    if grid_data[pos].Square_Type in [TILE_TYPE.COLLAPSED, TILE_TYPE.COLLAPSABLE, TILE_TYPE.OUTLINED]:
        return
    
    if grid_data[pos].Colour == target_color:                        
        neighbouring_squares = get_neighbouring_cross(pos, size, steps)
        grid_data[pos].Square_Type = TILE_TYPE.OUTLINED
        for square in neighbouring_squares:        
            process_blocks(square, size, target_color, steps)

def apply_collapsed(size, rows, cols):
    """from bottom row work way to top, row by row
       for each found collapsable block replace it with the block above it and pull
       it all down       
    """        
    move_left = False
    for col in range(0, cols): 
        blocks = [b for b in get_blocks_by_col(col, size, SQUARE_SIZE) if grid_data[b].Square_Type == TILE_TYPE.OUTLINED]        
        #collapse this column
        
        for b in blocks:              
            move_block_down(b, size)  #works brilliantly
        if does_col_need_left_shift(col, size):
            print(f"Moving col {col} left")
            move_col_left(col, size)

def move_block_down(pos, size):
    if grid_data[pos].Square_Type == TILE_TYPE.COLLAPSED:
        return

    if not has_top(pos, size):
        grid_data[pos].Colour = COLOURS.BLACK
        grid_data[pos].Square_Type = TILE_TYPE.COLLAPSED
        return    

    top = get_square_at((pos[0], pos[1] - SQUARE_SIZE))
    
    grid_data[pos].Colour = grid_data[top].Colour
    grid_data[pos].Square_Type = TILE_TYPE.VISIBLE
    
    move_block_down(top, size)
def does_col_need_left_shift(col, size):
    blocks = get_blocks_by_col(col, size, SQUARE_SIZE)    
    return len(blocks) == len([b for b in blocks if grid_data[b].Colour == COLOURS.BLACK])
    
def move_col_left(col, size):
    print(f"Checking col {col}")
    for r in range(ROWS):
        for c in range(COLS):
            pos = (c * SQUARE_SIZE, r * SQUARE_SIZE)
            pos_right = (c * SQUARE_SIZE, 1 + r * SQUARE_SIZE)        
            if not has_right(pos, size):
                grid_data[pos].Colour = COLOURS.BLACK
                grid_data[pos].Square_Type = TILE_TYPE.VISIBLE                
            else:            
                grid_data[pos].Colour = grid_data[pos_right].Colour
                grid_data[pos].Square_Type = TILE_TYPE.VISIBLE            
                grid_data[pos_right].Colour = COLOURS.BLACK
                grid_data[pos].Square_Type = TILE_TYPE.VISIBLE
   
def get_blocks_by_row(row, size, steps=10):
    cols = size[0] // steps #width
    rows = size[1] // steps #height
    if row > rows or row < 0:
        return []    
    blocks = []
    for r in range(cols):
        blocks.append(get_square_at((r * steps, row * steps)))    
    return [b for b in blocks]

def get_blocks_by_col(col, size, steps=10):
    cols = size[0] // steps #width
    rows = size[1] // steps #height
    if col > cols or col < 0:
        return []    
    blocks = []
    for r in range(rows):
        blocks.append(get_square_at((col * steps, r * steps)))    
    return [b for b in blocks]

def get_neighbouring_cross(pos, size, steps=10):
    pos = get_square_at(pos)
    squares = []
    if has_top(pos, size):
        squares.append(get_square_at((pos[0], pos[1]-steps))) #T        
    if has_bottom(pos, size, steps):
        squares.append(get_square_at((pos[0], pos[1]+steps))) #B        
    if has_right(pos, size, steps):
        squares.append(get_square_at((pos[0] + steps, pos[1])))  #R
    if has_left(pos, size, steps):
        squares.append(get_square_at((pos[0] - steps, pos[1])))  #L
    return squares

def get_neighbouring_squares(pos, size, steps=10):
    pos = get_square_at(pos)
    #T,TR,R,BR,B,BL,L,TL
    squares = []
    if has_top(pos, size):
        squares.append(get_square_at((pos[0], pos[1]-steps))) #T
        if has_left(pos, size, steps):
            squares.append(get_square_at((pos[0] - steps, pos[1] - steps)))  #TL
        if has_right(pos, size, steps):
            squares.append(get_square_at((pos[0] + steps, pos[1] - steps)))  #TR
    if has_bottom(pos, size, steps):
        squares.append(get_square_at((pos[0], pos[1]+steps))) #B
        if has_left(pos, size, steps):
            squares.append(get_square_at((pos[0] - steps, pos[1] + steps)))  #BL
        if has_right(pos, size, steps):
            squares.append(get_square_at((pos[0] + steps, pos[1] + steps)))  #BR
    if has_right(pos, size, steps):
        squares.append(get_square_at((pos[0] + steps, pos[1])))  #R
    if has_left(pos, size, steps):
        squares.append(get_square_at((pos[0] - steps, pos[1])))  #L
    return squares
    
def get_square_at(pos):        
    return size_manager.get_row_and_col_from_pos(pos)    
            
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
    
def create_level(size, grid_data):    
    for col in range(COLS):        
        for row in range(ROWS):            
            s = size_manager.get_pos_by_row_and_col(row,col)
            grid_data[(row,col)].Square_Type = TILE_TYPE.VISIBLE

def apply_left_shifts():

    pass
def update_score():
    s = f"SAME GAME{1}"
    pygame.display.set_caption("SAME GAME")
########################################################################################    
pygame.init()
ROWS = 10
COLS = 20
SQUARE_SIZE = 40

size_manager = BOARD_MANAGER(ROWS, COLS, SQUARE_SIZE)

# Set the width and height of the screen [width, height]
size = (size_manager.width, size_manager.height)

screen = pygame.display.set_mode((size[0]+2, size[1]+2)) 
 
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

create_level(size, grid_data) #fill with mines
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
            clicked_square = get_square_at(pos)
            print(f"Clicked square is: {clicked_square}")          
            clicked_row, clicked_col = size_manager.get_row_and_col_from_pos(pos)            
            
            if grid_data[clicked_square].Square_Type == TILE_TYPE.OUTLINED: #the user has clicked an outlined block                
                apply_collapsed(size, ROWS, COLS)                
                continue
                        
            for k in [m for m in grid_data if grid_data[m].Square_Type == TILE_TYPE.OUTLINED]:
                grid_data[k].Square_Type = TILE_TYPE.VISIBLE
            
            process_blocks(clicked_square, size, grid_data[clicked_square].Colour, SQUARE_SIZE)  #the game runs inside this                        
            
            
            #update_score()
    # --- Game logic should go here
    
    # --- Screen-clearing code goes here          
    screen.fill(COLOURS.BLACK)
 
    # --- Drawing code should go here        (update game visuals / no logic here!)
    # draw a grid    
    draw_grid(screen, size, SQUARE_SIZE)
    
    #update grid
    
    for k in grid_data:              
        pos = size_manager.get_pos_by_row_and_col(k[1], k[0])
        print(pos)
        pygame.draw.rect(screen, grid_data[k].Colour, [pos[1] + 1, pos[0] + 1, SQUARE_SIZE - 3, SQUARE_SIZE - 2])
    
    for k in [m for m in grid_data if grid_data[m].Square_Type == TILE_TYPE.OUTLINED]:
        marker_size = SQUARE_SIZE // 2
        pygame.draw.rect(screen, COLOURS.BLACK, [k[0] + marker_size//2, k[1] + marker_size//2, marker_size, marker_size])            
    
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to x frames per second
    clock.tick(10)
 
# Close the window and quit.
pygame.quit()