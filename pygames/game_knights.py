#!/usr/bin/env python

import pygame
import random
import sys
import abc
from enum import Enum
from collections import defaultdict
from utils import POS, DIRECTIONS, COLOURS 
from game_utils import BOARD_MANAGER

class KNIGHT_DIRECTIONS:
    TWO_RIGHT_ONE_DOWN = POS(2, 1)
    ONE_RIGHT_TWO_DOWN = POS(1, 2)   
    ONE_LEFT_TWO_DOWN = POS(-1, 2)
    TWO_LEFT_ONE_DOWN = POS(-2, 1)
    TWO_LEFT_ONE_UP = POS(-2, -1)    
    ONE_LEFT_TWO_UP = POS(-1, -2)
    ONE_RIGHT_TWO_UP = POS(1, -2)    
    TWO_RIGHT_ONE_UP = POS(2, -1)

grid_data = {}

visited = []
tovisit = []

def is_visited(p):
    return p in visited

def is_valid_placement(n, IgnorePlaced=False):    
    return n.r < ROWS and n.c < ROWS and n.r >= 0 and n.c >= 0 and (IgnorePlaced or knights[(n.r, n.c)] == -1)  and not is_visited(n)

#this sequence causing the knight to explore a position in a circular fashion, important for the optimization!    
knight_next = [KNIGHT_DIRECTIONS.TWO_RIGHT_ONE_DOWN, KNIGHT_DIRECTIONS.ONE_RIGHT_TWO_DOWN, KNIGHT_DIRECTIONS.ONE_LEFT_TWO_DOWN, \
            KNIGHT_DIRECTIONS.TWO_LEFT_ONE_DOWN, KNIGHT_DIRECTIONS.TWO_LEFT_ONE_UP, KNIGHT_DIRECTIONS.ONE_LEFT_TWO_UP, \
                KNIGHT_DIRECTIONS.ONE_RIGHT_TWO_UP, KNIGHT_DIRECTIONS.TWO_RIGHT_ONE_UP]

#this sequence causing the knight to explore a position in a circular fashion, important for the optimization!
knight_next = [POS(2,1), POS(1,2), POS(-1,2), POS(-2,1), POS(-2,-1), POS(-1,-2), POS(1,-2), POS(2,-1)]


def get_valid_moves(p, IgnorePlaced=False):
    valid_moves = []
    #valid_moves.append(p)
    for kn in knight_next:        
        if is_valid_placement(p + kn, IgnorePlaced):
            if not (p + kn) == p:                
                valid_moves.append(p+kn)        
    return valid_moves



def get_sorted_valid_moves(moves):
    return sorted(moves, key=lambda m:len(get_valid_moves(m)))

solved = False
def solve(startPos, moveNumber):
    knights[(startPos.r, startPos.c)] = moveNumber    
    if (moveNumber) == (ROWS**2):            
        solved = True
        return True   
    valid_moves = get_valid_moves(startPos)
    valid_moves = get_sorted_valid_moves(valid_moves)    
    for move in valid_moves:        
        if (is_valid_placement(move)):            
            if solve( move, moveNumber+1):                            
                return True                
            else:                                                
                knights[(move.r, move.c)] = -1    
    return False
results = {}

def fibmemo(n):
    result = 0
    if n == 1:
        return n
    if n not in results:
        result = n * fib(n - 1)
        results[n] = result
    else:
        result = results[n]
    return result

def fib(n):    
    if n == 1:
        return n    
    return n * fib(n - 1)        

def solveNonRecursively():
    moveNumber = 1
    pos  = POS(0, 0)    
    solved = False
    current_square = pos
    visited.append(current_square)    
    while not solved:  #while there are positions to visit                        
        knights[(current_square.r, current_square.c)] = moveNumber
        yield
        valid_moves = get_valid_moves(current_square, True) #get valid moves, ignore placed
        valid_moves = get_sorted_valid_moves(valid_moves)  #sort the valid moves to select next           
        for m in valid_moves:                        
            if m in visited:
                moveNumber -= 1
                visited.pop()
                print("Popping backward")             
                continue
            else:
                current_square = m                
                moveNumber += 1                
                visited.append(current_square)
                break        
        if len(visited) == ROWS * ROWS:
            print(visited)
            solved = True
            knights[(current_square.r, current_square.c)] = moveNumber                                

########################################################################################
ROWS = 100
SQUARE_SIZE = 30

board_manager = BOARD_MANAGER(ROWS, ROWS, SQUARE_SIZE)

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# game variables
BUTTON_LEFT = 1
BUTTON_RIGHT = 3

knights = defaultdict(lambda: -1)
pygame.init()
#knights[(0, 0)] = 0
#solve(POS(0,0), 1)
#solveNonRecursively()
solver = solveNonRecursively()

# -------- Main Program Loop -----------
# Game().run()

#solve(POS(0,0),1)
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
            clicked_square = board_manager.get_row_and_col_from_pos(pos)
            clicked_row, clicked_col = board_manager.get_row_and_col_from_pos(pos)

            print(f"You clicked row {clicked_row} and col {clicked_col}")
            knights.clear()
            v = get_valid_moves(POS(clicked_row, clicked_col))
            #v = get_sorted_valid_moves(v) 
            for index, k in enumerate(v):
                print(index,k)
                knights[(k.r, k.c)] = str(index)
                pos = board_manager.get_pos_by_row_and_col(k.r,k.c)
                #draw_text_in_block(str(i),(pos[0], pos[1]),screen)

    # --- Game logic should go here    
    if not solved:
        try:
            solver.__next__()
        except StopIteration:
            solved=  True
            print("solved")
            pass
    # --- Screen-clearing code goes here
    board_manager.screen.fill(COLOURS.BLACK)

    # --- Drawing code should go here        (update game visuals / no logic here!)
    # draw a grid
    board_manager.draw_grid()

    # update grid

    for k in grid_data:
        pos = board_manager.get_pos_by_row_and_col(k[0], k[1])
        pygame.draw.rect(board_manager.screen, grid_data[k].Colour, [
                         pos[0] + 1, pos[1] + 1, SQUARE_SIZE - 1, SQUARE_SIZE - 1])

    for k in knights:
        if knights[k]:
            pos = board_manager.get_pos_by_row_and_col(k[0], k[1])
            if not knights[k] == -1:
                board_manager.draw_text_in_block(str(knights[k]), (pos[0], pos[1]))
                
            #pygame.draw.circle(screen, COLOURS.GREEN, [
            #                   pos[0] + SQUARE_SIZE // 2, pos[1] + SQUARE_SIZE // 2], SQUARE_SIZE // 4)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to x frames per second
    clock.tick(10)

# Close the window and quit.
pygame.quit()

"""
start somewhere
find valid moves
if teh valid
"""