from pprint import pprint
import keyboard
from random import sample
import os
from time import sleep
import sys
from copy import deepcopy

from blocks import BLOCKS

# while True:
    # left, right, up, down, space

board = [[0 for _ in range(10+8)] for _ in range(20+8)]

block_reach = []

def generate_new_block():
    new_block = sample(list(BLOCKS.keys()), k=1)[0]
    # new_block = "I"
    start_x, start_y = 7, 0

    for i in range(5):
        if is_ok([start_x, i, new_block, 0], action="down"): continue
        else: break

    start_y = i

    return [start_x, start_y, new_block, 0]


def print_board(current_block):

    os.system("clear")
    print(f"---- SCORE: {score} ----", end="\n\n")

    x, y, block, direction = current_block
    block_matrix = BLOCKS[block][direction]
    for i in range(4, 24):
        for j in range(4, 14):
            if y <= i and i < y+4 and x <= j and j < x+4:
                if board[i][j] == 1: print("#", end=" ")
                else:
                    if block_matrix[i-y][j-x]: print("#", end=" ")
                    else: print("-", end=" ")
                    # print(block_matrix[i-y][j-x], end=" ")

            else:
                if board[i][j]: print("#", end=" ")
                else:
                    print("-", end=" ")
                # print(board[i][j], end=" ")

        print(end="\n")

    sleep(0.075)

def is_gameover():
    # pprint(board)
    for i in range(5):
        if 1 in board[i]: return True

    # sys.exit(0)

    return False

def get_completed_line():
    line_index = []

    for i in range(4, 24):
        if board[i] == [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0]:
            line_index.append(i)

    return line_index
            

def is_overlapped(block_matrix, x, y):
    for i in range(4):
        for j in range(4):
            if board[y+i][x+j] == 1 and block_matrix[i][j] == 1:
                return True
    
    return False


def is_ok(current_block, action):
    x, y, block, direction = current_block
    block_matrix = BLOCKS[block][direction]

    if action == "left":
        left_x = x
        is_break = False

        for x_ in range(4):
            for y_ in range(4):
                if block_matrix[y_][x_] == 1:
                    is_break = True
                    break
            
            if is_break: break

        left_x += x_

        # print(block_matrix)
        # print(left_x)
        # sys.exit(0)

        if left_x == 4 or is_overlapped(block_matrix, x-1, y): return False

        return True

    
    elif action == "right":
        right_x = x
        is_break = False

        for x_ in range(3, -1, -1):
            for y_ in range(4):
                if block_matrix[y_][x_] == 1:
                    is_break = True
                    break
            
            if is_break: break
        
        right_x += x_

        if right_x == 13 or is_overlapped(block_matrix, x+1, y): return False

        return True
    
    elif action == "up":
        rotated_block_matrix = BLOCKS[block][(direction+1)%4]
        
        for i in range(4):
            for j in range(4):
                if x+j < 4 or 13 < x+j or 23 < y+i:
                    if rotated_block_matrix[i][j] == 1: return False
        
        if is_overlapped(rotated_block_matrix, x, y): return False

        return True

    elif action == "down":
        bottom_y = y

        for i in range(3, -1, -1):
            if 1 in block_matrix[i]:
                break
        
        bottom_y += i

        if bottom_y == 23 or is_overlapped(block_matrix, x, y+1): return False

        return True

    elif action == "space":
        return True


def construct_block(current_block):
    global board
    x, y, block, direction = current_block
    block_matrix = BLOCKS[block][direction]
    for i in range(4):
        for j in range(4):
            # print(i, j)
            if block_matrix[i][j] == 1:
                board[y+i][x+j] = 1

def step(action):
    global current_block, score
    
    if is_ok(current_block, action):

        if action == "left":
            current_block[0] -= 1

        elif action == "right":
            current_block[0] += 1
        
        elif action == "up":
            current_block[3] = (current_block[3] + 1) % 4
        
        elif action == "down":
            current_block[1] += 1
        
        elif action == "space":
            if not is_ok(current_block, action="down"):
                block_reach.append(1)

            else:
                for i in range(20):
                    if not is_ok([current_block[0], current_block[1]+i, current_block[2], current_block[3]], action="down"):
                        break

                current_block[1] += i

            block_reach.extend([1, 1])
    
    print_board(current_block)

    if score >= 10:
        os.system("clear")
        print(f"------- SUCCESS! -------")
        print(f"---- SCORE: {score} ----")
        sys.exit(0)       

    if is_ok(current_block, action="down"):
        current_block[1] += 1
        print_board(current_block)
    
    else:
        if block_reach[-3:].count(1) == 3:
            construct_block(current_block)

            # gameover = is_gameover()
            # print(gameover)

            # if len(cnt) > 9:
            #     pprint(board)
            #     sys.exit(0)

            if is_gameover():
                print("------ GAME OVER! ------")
                print(f"---- SCORE: {score} ----")
                sys.exit(0)
            
            completed_line = get_completed_line()

            for line_index in completed_line:
                temp_arr = board[:line_index]
                board[:line_index] = [[0 for _ in range(10+8)] for _ in range(line_index)]
                board[1:line_index+1] = temp_arr
                # pprint(board)

                # for i in range(len(temp_arr)):
                #     board[i+1] = temp_arr[i]

                score += 1

            # generate new block
            current_block = generate_new_block()
            cnt.append(0)
            block_reach.append(0)
        
        else:
            block_reach.append(1)

cnt = [0]
score = 0
current_block = generate_new_block()

print_board(current_block)

action_list = ["left", "right", "up", "down", "space"]
while True:
    action = None
    for act in action_list:
        if keyboard.is_pressed(act): action = act

    step(action)