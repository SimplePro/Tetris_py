from pprint import pprint
import keyboard
from random import sample
import os
from time import sleep

from blocks import BLOCKS

# while True:
    # left, right, up, down, space

board = [[0] * (10+6)] * (20+6)

block_reach = []

def generate_new_block():
    new_block = sample(list(BLOCKS.keys()), k=1)[0]
    block_matrix = BLOCKS[new_block][0]

    start_x, start_y = 6, 3
    for i in range(4):
        if 1 in block_matrix[i]:
            print(i, block_matrix, new_block)
            start_y -= i
            break

    return [start_x, start_y, new_block, 0]


def print_board(current_block):
    x, y, block, direction = current_block
    block_matrix = BLOCKS[block][direction]
    os.system("clear")
    for i in range(3, 23):
        for j in range(3, 13):
            if y <= i and i < y+4 and x <= j and j < x+4:
                print(block_matrix[i-y][j-x], end=" ")
                # print(i, j)
                # print("1", end=" ")

            else:
                print(board[i][j], end=" ")

        print(end="\n")

    sleep(750)

def is_ok(block, action):
    pass

def step(action):
    global current_block, score
    
    if action == "left":
        current_block[0] -= 1

    elif action == "right":
        current_block[0] += 1
    
    elif action == "up":
        current_block[3] = (current_block[3] + 1) % 4
    
    elif action == "down":
        current_block[1] += 1
    
    elif action == "space":
        for i in range(20):
            if is_ok([current_block[0], current_block[1]+i, current_block[2], current_block[3]], action="down"):
                continue
        
            else:
                break

        current_block[1] += i+1
    
    print_board()

    if is_ok(current_block, action="down"):
        current_block[1] += 1
        print_board()
    
    else:
        if block_reach[-3:].count(1) == 3:
            # one line complete?
            # game over?

            # generate new block
            current_block = generate_new_block
        pass

score = 0
current_block = generate_new_block()

print_board(current_block)
