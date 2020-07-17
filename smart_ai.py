#!/usr/bin/env python3
# -*- coding: utf-8 -*

"""
COMS W4701 Artificial Intelligence - Programming Homework 2

An AI player for Othello. This is the template file that you need to  
complete and submit. 

@author: Elliot Lee UNI:esl2167
"""

import random
import sys
import time

# You can use the functions in othello_shared to write your AI 
from othello_shared import find_lines, get_possible_moves, get_score, play_move

def compute_utility(board, color):
    scores = get_score(board)
    if color==1:
      utility = scores[0]-scores[1]
    else:
      utility = scores[1] - scores[0]
    return utility

def modified_score(board, color): #extra score for corners
    p1_count = 0
    p2_count = 0
    length = len(board)
    for i in range(length):
        for j in range(length):
            if board[i][j] == 1:
                if (i == 0 or i== length-1) and (j==0 or j==length-1):
                  p1_count += 3
                else:
                  p1_count+=1
            elif board[i][j] == 2:
                if (i == 0 or i== length-1) and (j==0 or j==length-1):
                  p2_count +=3
                else:
                  p2_count += 1
    if color==1:
      utility = p1_count - p2_count
    else:
      utility = p2_count -p1_count
    return utility

def modified_score2(board, color): #looks at corners and spaces around corners
    #score hierarchy:
    #Spaces around a corner without the corner: -1
    #Normal Space: 1
    #Spaces around a corner with the corner: 2
    #Corners: 3
    p1_count = 0
    p2_count = 0
    length = len(board)

    corner_space = {
      (0,0) : [(0,1),(1,0),(1,1)],
      (0,length-1) :[(0, length-2), (1,length-1), (1,length-2)],
      (length-1,0): [(length-2, 0), (length-1, 1), (length-2, 1)],
      (length-1,length-1): [(length-2, length-1), (length-1, length-2), (length-2, length-2)]
    }

    corners = {(0,1),(1,0),(1,1), (length-2, 0), (length-1, 1), (length-2, 1), (length-2, 0), (length-1, 1), (length-2, 1),(length-2, length-1), (length-1, length-2), (length-2, length-2)}
    #corner_space[(0,0)] = [(0,1),(1,0),(1,1)]
    #corner_space[(0,length-1)] = [(0, length-2), (1,length-1), (1,length-2)]
    #corner_space[(length-1,0)] = []
    #corner_space[(length-1,length-1)] = []
    for i in range(length):
        for j in range(length):
            if board[i][j] == 1:
                if (i == 0 or i== length-1) and (j==0 or j==length-1):
                  p1_count += 3
                  for x in corner_space[(i,j)]:
                    if board[x[0]][x[1]] ==1:
                      p1_count+=3
                elif {(i,j)}.issubset(corners):
                  p1_count -=1
                else:
                  p1_count+=1
            elif board[i][j] == 2:
                if (i == 0 or i== length-1) and (j==0 or j==length-1):
                  p2_count +=3
                  for x in corner_space[(i,j)]:
                    if board[x[0]][x[1]] ==2:
                      p2_count+=3
                elif {(i,j)}.issubset(corners):
                  p2_count -=1
                else:
                  p2_count += 1
    if color==1:
      utility = p1_count - p2_count
    else:
      utility = p2_count -p1_count
    return utility

############ MINIMAX ###############################

def minimax_min_node(board, color):
    moves = get_possible_moves(board, color)
    #values = []
    currentMin = 2147483647
    new = []
    if len(moves)==0:
      if color ==1:
        color=2
      else:
        color =1
      return compute_utility(board, color)
    for x in range(len(moves)):
      new.append(play_move(board, color, moves[x][0], moves[x][1]))
    if color ==1:
      color=2
    else:
      color =1
    for x in new:
      temp = minimax_max_node(x, color)
      if temp<currentMin:
        currentMin = temp
      #values.append(minimax_max_node(x, color))
    #values.sort()
    return currentMin

def minimax_max_node(board, color):
    moves = get_possible_moves(board, color)
    new = []
    #values = []
    currentMax = -2147483647
    if len(moves)==0:
      return compute_utility(board, color)
    for x in range(len(moves)):
        new.append(play_move(board, color, moves[x][0], moves[x][1]))
    if color ==1:
      color=2
    else:
      color =1
    for x in new:
      temp = minimax_min_node(x, color)
      if temp>currentMax:
        currentMax = temp
      #values.append(minimax_min_node(x, color))
    #values.sort()
    return currentMax
    #python othello_gui.py lessSmart_ai.py smart_ai.py
    #python othello_gui.py smart_ai.py lessSmart_ai.py  
    #python othello_gui.py randy_ai.py smart_ai.py
    #python othello_gui.py smart_ai.py

def minimax_min_node2(board, color, level, limit, heuristic):
    moves = get_possible_moves(board, color)
    #values = []
    currentMin = 2147483647
    new = []
    if len(moves)==0:
      if color ==1:
        color=2
      else:
        color =1
      return compute_utility(board, color)
    for x in range(len(moves)):
      new.append(play_move(board, color, moves[x][0], moves[x][1]))
    if color ==1:
      color=2
    else:
      color =1
    if level==limit:
      for x in new:
        temp = heuristic(x, color)
        if temp<currentMin:
          currentMin = temp
    else:
      level+=1
      for x in new:
        temp = minimax_max_node2(x, color, level, limit, heuristic)
        if temp<currentMin:
          currentMin = temp
      #values.append(minimax_max_node(x, color))
    #values.sort()
    return currentMin

def minimax_max_node2(board, color, level, limit, heuristic):
    moves = get_possible_moves(board, color)
    new = []
    #values = []
    currentMax = -2147483647
    if len(moves)==0:
      return compute_utility(board, color)
    for x in range(len(moves)):
        new.append(play_move(board, color, moves[x][0], moves[x][1]))
    if level==limit:
      for x in new:
        temp = heuristic(x, color)
        if temp>currentMax:
          currentMax = temp
    else:
      level +=1
      if color ==1:
        color=2
      else:
        color =1
      for x in new:
        temp = minimax_min_node2(x, color, level, limit, heuristic)
        if temp>currentMax:
          currentMax = temp
      #values.append(minimax_min_node(x, color))
    #values.sort()
    return currentMax
 


def select_move_minimax(board, color):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  
    """
    #values = []
    currentHigh = -2147483647, (9999,9999)
    temp = 0
    new = []
    moves = get_possible_moves(board, color)
    for x in range(len(moves)):
        new.append((play_move(board, color, moves[x][0], moves[x][1]), moves[x]))
    if color ==1:
      color=2
    else:
      color =1

    for x in new:
      temp = (minimax_min_node2(x[0], color,1, 3, modified_score2),x[1])
      if temp[0] >currentHigh[0]:
        currentHigh = temp
      #values.append((minimax_min_node(x[0], color),x[1]))
      #values.sort()
    return currentHigh[1]
    
############ ALPHA-BETA PRUNING #####################

#alphabeta_min_node(board, color, alpha, beta, level, limit)
def alphabeta_min_node(board, color, alpha, beta): 
    return None


#alphabeta_max_node(board, color, alpha, beta, level, limit)
def alphabeta_max_node(board, color, alpha, beta):
    return None


def select_move_alphabeta(board, color): 
    return 0,0 


####################################################
def run_ai():
    """
    This function establishes communication with the game manager. 
    It first introduces itself and receives its color. 
    Then it repeatedly receives the current score and current board state
    until the game is over. 
    """
    print("Big Brain AI") # First line is the name of this AI  
    color = int(input()) # Then we read the color: 1 for dark (goes first), 
                         # 2 for light. 

    while True: # This is the main loop 
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input() 
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over. 
            print 
        else: 
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The 
                                  # squares in each row are represented by 
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)
                    
            # Select the move and send it to the manager 
            movei, movej = select_move_minimax(board, color)
            #movei, movej = select_move_alphabeta(board, color)
            print("{} {}".format(movei, movej)) 


if __name__ == "__main__":
    run_ai()
