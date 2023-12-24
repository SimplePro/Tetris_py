import keyboard
from random import randint
import os
from time import sleep, time

from blocks import BLOCKS


frame_count = []
t = 0

# (20+8) x (10+8) size
board = []

for i in range(20+8):
    temp_arr = []
    for j in range(10+8):
        temp_arr.append(0)

    board.append(temp_arr)

# is current_block reached
block_reach = []

block_list = []

for i in range(2):
    block_list.append(
        randint(0, len(BLOCKS)-1)
    )

# generate new random block 
def generate_new_block():
    new_block = block_list[-2]
    block_list.append(
        randint(0, len(BLOCKS)-1)
    )

    start_x, start_y = 7, 0

    for i in range(5):
        if not is_ok([start_x, i, new_block, 0], action="down"): break

    start_y = i

    return [start_x, start_y, new_block, 0]

# print board with current_block
def print_board(current_block):

    global t

    t = time() - start_time

    os.system("clear")
    print(f"----- USER: {student_name} -----")
    print(f"---- SCORE: {score}, TIME: {round(t, 4)} ----", end="\n\n")

    print(f"---- NEXT BLOCK ----", end="\n\n")
    next_block_matrix = BLOCKS[block_list[-2]][0]
    for i in range(4): 
        print("    ", end="")
        for j in range(4):
            if next_block_matrix[i][j] == 1: print("O", end=" ")
            else: print("-", end=" ")
        print(end="\n")
    
    print(end="\n\n\n")

    x, y, block, direction = current_block
    block_matrix = BLOCKS[block][direction]
    for i in range(4, 24):
        for j in range(4, 14):
            if y <= i and i < y+4 and x <= j and j < x+4:
                if board[i][j] == 1: print("O", end=" ")
                else:
                    if block_matrix[i-y][j-x]: print("O", end=" ")
                    else: print("-", end=" ")

            else:
                if board[i][j]: print("O", end=" ")
                else:
                    print("-", end=" ")

        print(end="\n")

    sleep(0.075)
    frame_count.append(0)

# is gameover
def is_gameover():
    for i in range(5):
        if 1 in board[i]: return True

    return False

# get complete line index
def get_completed_line():
    line_index = []

    for i in range(4, 24):
        if board[i] == [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0]:
            line_index.append(i)

    return line_index

# current_block and other blocks are overlapped
def is_overlapped(block_matrix, x, y):
    for i in range(4):
        for j in range(4):
            if board[y+i][x+j] == 1 and block_matrix[i][j] == 1:
                return True
    
    return False

# is action ok
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


# construct current_block in board
def construct_block(current_block):
    global board
    x, y, block, direction = current_block
    block_matrix = BLOCKS[block][direction]
    for i in range(4):
        for j in range(4):
            if block_matrix[i][j] == 1:
                board[y+i][x+j] = 1

# step per frame
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
        print(f"------- SUCCESS! -------")
        print(f"---- SCORE: {score}, TIME: {round(t, 4)} ----")
        return True

    if is_ok(current_block, action="down"):
        if len(frame_count) % 3 == 0:
            current_block[1] += 1
            print_board(current_block)
    
    else:
        if block_reach[-6:].count(1) == 6:
            construct_block(current_block)

            if is_gameover():
                print("------ GAME OVER! ------")
                print(f"---- SCORE: {score}, TIME: {round(t, 4)} ----")
                return True
            
            completed_line = get_completed_line()

            for line_index in completed_line:
                temp_arr = board[:line_index]
                board[:line_index] = [[0 for _ in range(10+8)] for _ in range(line_index)]
                board[1:line_index+1] = temp_arr

                score += 1

            current_block = generate_new_block()
            block_reach.append(0)
        
        else:
            block_reach.append(1)

    return False

os.system("clear")
print("---------- 1학년 14반 테트리스 게임 ----------")
attendance_index = int(input("출석번호 입력: ")) - 1

students = []

with open("students.txt", "r") as f:
    for line in f.readlines():
        name, t_ = line.split()
        students.append([name, float(t_)])

student_name, student_t = students[attendance_index]

print(f"안녕하세요 {student_name}님")

if student_t == -1:
    print(f"현재 {student_name}님의 기록은 없습니다.")
else:
    print(f"현재 {student_name}님의 기록은 {round(student_t, 4)}초입니다.")

for i in range(1, 4):
    print("\r%d"%(4-i), end="")
    sleep(1)

start_time = time()

score = 0
current_block = generate_new_block()

print_board(current_block)

action_list = ["left", "right", "up", "down", "space"]
while True:
    action = None
    for act in action_list:
        if keyboard.is_pressed(act): action = act

    is_quit = step(action)
    if is_quit: break

if score >= 10:
    end_time = time()

    if t < student_t or student_t == -1:
        students[attendance_index][1] = t

        s = ""

        for i in range(len(students)):
            s += f"{students[i][0]} {students[i][1]}"

            if i != len(students)-1:
                s += "\n"
        
        with open("students.txt", "w") as f:
            f.write(s)
            
        print(f"기록이 {round(t, 4)}초로 갱신되었습니다.")