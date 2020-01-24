#!/usr/bin/env python

import pygame
import random
import sys
import abc
from enum import Enum
from collections import defaultdict
from utils import POS, DIRECTIONS, COLOURS

class KNIGHT_DIRECTIONS:
    BR = POS(2, 1)
    RB = POS(1, 2)   
    RT = POS(-1, 2)
    TR = POS(-2, 1)
    TL = POS(-2, -1)    
    LT = POS(-1, -2)
    LB = POS(1, -2)    
    BL = POS(2, -1)

class TILE_DATA:
    def __init__(self, v, c):
        self.visited = v
        self.c = c

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


grid_data = {}


def get_square_at(pos):
    return size_manager.get_row_and_col_from_pos(pos)


def draw_grid(screen):
    for x in range(size_manager.rows+1):
        pygame.draw.line(screen, COLOURS.WHITE, size_manager.get_pos_by_row_and_col(
            x, 0), size_manager.get_pos_by_row_and_col(x, size_manager.cols), 1)
        for y in range(size_manager.cols+1):
            pygame.draw.line(screen, COLOURS.WHITE, size_manager.get_pos_by_row_and_col(
                0, y), size_manager.get_pos_by_row_and_col(size_manager.rows, y), 1)


def draw_text_in_block(text, pos, screen, font_size=11):
    font = pygame.font.Font("freesansbold.ttf", font_size)
    t = font.render(text, True, COLOURS.BLACK, COLOURS.WHITE)
    textRect = t.get_rect()
    textRect.center = ((pos[0] + SQUARE_SIZE // 2),
                       (pos[1] + SQUARE_SIZE // 2))
    screen.blit(t, textRect)


def is_visited(p):
    return p in visited

def is_valid_placement(n, knights):    
    return n.r < ROWS and n.c < ROWS and n.r >= 0 and n.c >= 0 and knights[(n.r, n.c)] == -1    
    
knight_next = [
            KNIGHT_DIRECTIONS.RB,
            KNIGHT_DIRECTIONS.BR,            
            KNIGHT_DIRECTIONS.RT,
            KNIGHT_DIRECTIONS.TR,
            KNIGHT_DIRECTIONS.TL,
            KNIGHT_DIRECTIONS.LT,
            KNIGHT_DIRECTIONS.LB,
            KNIGHT_DIRECTIONS.BL]
#this sequence causing the knight to explore a position in a circular fashion, important for the optimization!
knight_next = [POS(2,1), POS(1,2), POS(-1,2), POS(-2,1), POS(-2,-1), POS(-1,-2), POS(1,-2), POS(2,-1)]

def get_valid_moves(p):
    valid_moves = []
    valid_moves.append(p)
    for kn in knight_next:        
        if is_valid_placement(p+kn, knights):
            valid_moves.append(p+kn)        
    return valid_moves

def get_sorted_valid_moves(moves):
    return sorted(moves, key=lambda m:len(get_valid_moves(m)))

def solve(startPos, moveNumber):
    knights[(startPos.r, startPos.c)] = moveNumber
    if (moveNumber) == (ROWS**2):    
        print(f"Solved at {moveNumber}")        
        return True            
    valid_moves = get_valid_moves(startPos)
    valid_moves = get_sorted_valid_moves(valid_moves)    
    for move in valid_moves:                
        if (is_valid_placement(move, knights)):            
            if solve( move, moveNumber+1):                            
                return True
            else:                                                
                knights[(move.r, move.c)] = -1    
    return False

solved = False

def solveNonRecursively():
    startPos = POS(0, 0)
    moveNumber = 1
    global solved 
    while True and not solved:        
        v = get_sorted_valid_moves(get_valid_moves(startPos))
        for move in v:
            if is_valid_placement(move):                                
                moveNumber += 1
                solved = moveNumber == ROWS * ROWS
            else:
                moveNumber -= 1
                knights[(move.r, move.c)] = -1
            
    print("Solved.")

########################################################################################
ROWS = 31
SQUARE_SIZE = 30

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

visited = defaultdict(lambda: False)
knights = defaultdict(lambda: -1)
pygame.init()
knights[(0, 0)] = 1
solve(POS(0,0), 1)
#solve(knights, POS(0,0), 1)
#solveNonRecursively()
# -------- Main Program Loop -----------
# Game().run()
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

            print(f"You clicked row {clicked_row} and col {clicked_col}")
            knights.clear()
            v = get_valid_moves(POS(clicked_row, clicked_col))
            #v = get_sorted_valid_moves(v) 
            for index, k in enumerate(v):
                print(index,k)
                knights[(k.r, k.c)] = str(index)
                pos = size_manager.get_pos_by_row_and_col(k.r,k.c)
                #draw_text_in_block(str(i),(pos[0], pos[1]),screen)

    # --- Game logic should go here
    
    # --- Screen-clearing code goes here
    screen.fill(COLOURS.BLACK)

    # --- Drawing code should go here        (update game visuals / no logic here!)
    # draw a grid
    draw_grid(screen)

    # update grid

    for k in grid_data:
        pos = size_manager.get_pos_by_row_and_col(k[0], k[1])
        pygame.draw.rect(screen, grid_data[k].Colour, [
                         pos[0] + 1, pos[1] + 1, SQUARE_SIZE - 1, SQUARE_SIZE - 1])

    for k in knights:
        if knights[k]:
            pos = size_manager.get_pos_by_row_and_col(k[0], k[1])
            if not knights[k] == -1:
                draw_text_in_block(str(knights[k]),(pos[0] , pos[1]),screen)
            #pygame.draw.circle(screen, COLOURS.GREEN, [
            #                   pos[0] + SQUARE_SIZE // 2, pos[1] + SQUARE_SIZE // 2], SQUARE_SIZE // 4)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to x frames per second
    clock.tick(10)

# Close the window and quit.
pygame.quit()
