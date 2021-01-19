import os
import tkinter
from tkinter import filedialog
import numpy as np
import pygame

from button import button
from img_processing import img_processing

pygame.init()
######################################################################################################
# preaparing boards

levels = [
    [
        [0, 0, 5, 0, 0, 0, 0, 0, 4],
        [7, 0, 4, 0, 9, 8, 0, 2, 0],
        [0, 0, 0, 0, 6, 0, 0, 0, 0],
        [5, 0, 0, 4, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 7, 0],
        [1, 0, 7, 6, 0, 0, 0, 0, 2],
        [0, 0, 0, 2, 0, 6, 0, 1, 8],
        [0, 0, 0, 3, 0, 0, 0, 0, 0],
        [9, 2, 0, 8, 0, 0, 4, 0, 0]
    ],

    [
        [0, 0, 5, 0, 0, 0, 0, 0, 4],
        [7, 0, 4, 0, 9, 8, 0, 2, 0],
        [0, 0, 0, 0, 6, 0, 0, 0, 0],
        [5, 0, 0, 4, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 7, 0],
        [1, 0, 7, 6, 0, 0, 0, 0, 2],
        [0, 0, 0, 2, 0, 6, 0, 1, 8],
        [0, 0, 0, 3, 0, 0, 2, 0, 0],
        [9, 2, 0, 8, 0, 0, 4, 0, 0]
    ],
    [
        [9, 5, 7, 0, 0, 0, 0, 0, 1],
        [0, 0, 8, 0, 5, 0, 4, 0, 0],
        [0, 4, 0, 8, 0, 1, 0, 0, 0],
        [0, 1, 3, 4, 9, 0, 7, 0, 6],
        [4, 0, 0, 0, 8, 0, 0, 0, 5],
        [8, 0, 5, 0, 6, 2, 3, 4, 0],
        [0, 0, 0, 2, 0, 9, 0, 3, 0],
        [0, 0, 2, 0, 4, 0, 1, 0, 0],
        [6, 0, 0, 0, 0, 0, 5, 7, 2],
    ]
]


#####################################################################################################
# solver algorithm
def check(y, x, n, board):
    global board

    for i in range(0, 9):
        if num[y][i] == n:
            return False
    for i in range(0, 9):
        if num[i][x] == n:
            return False
    x0 = (x // 3) * 3
    y0 = (y // 3) * 3
    for i in range(0, 3):
        for j in range(0, 3):
            if num[y0 + i][x0 + j] == n:
                return False
    return True


def solve():
    global num, completed_board
    for y in range(9):
        for x in range(9):
            if num[y][x] == 0:
                for n in range(1, 10):
                    if check(y, x, n):
                        num[y][x] = n
                        solve()
                        num[y][x] = 0
                return
    ###########################################################################################
    array = np.array(num)
    with open('solved.txt', 'wb')as f:
        np.save(f, array)

    with open('solved.txt', 'rb') as f:
        completed_board = np.load(f).tolist()


# GUI
################################################################################################################
black_x = pygame.image.load('imgs/black_X.png')
red_x = pygame.image.load('imgs/red_X.png')


def drawing_play_board():
    pygame.draw.rect(board, (0, 0, 0), (20, 50, 472, 4))
    pygame.draw.rect(board, (0, 0, 0), (20, 206, 472, 4))
    pygame.draw.rect(board, (0, 0, 0), (20, 362, 472, 4))
    pygame.draw.rect(board, (0, 0, 0), (20, 518, 472, 4))

    ############################################################################
    pygame.draw.rect(board, (0, 0, 0), (20, 104, 472, 1))
    pygame.draw.rect(board, (0, 0, 0), (20, 155, 472, 1))

    pygame.draw.rect(board, (0, 0, 0), (20, 260, 472, 1))
    pygame.draw.rect(board, (0, 0, 0), (20, 311, 472, 1))

    pygame.draw.rect(board, (0, 0, 0), (20, 416, 472, 1))
    pygame.draw.rect(board, (0, 0, 0), (20, 467, 472, 1))
    #############################################################################

    pygame.draw.rect(board, (0, 0, 0), (20, 50, 4, 522 - 50))
    pygame.draw.rect(board, (0, 0, 0), (176, 50, 4, 522 - 50))
    pygame.draw.rect(board, (0, 0, 0), (332, 50, 4, 522 - 50))
    pygame.draw.rect(board, (0, 0, 0), (488, 50, 4, 522 - 50))

    #####################################################################################
    pygame.draw.rect(board, (0, 0, 0), (74, 50, 1, 522 - 50))
    pygame.draw.rect(board, (0, 0, 0), (125, 50, 1, 522 - 50))

    pygame.draw.rect(board, (0, 0, 0), (230, 50, 1, 522 - 50))
    pygame.draw.rect(board, (0, 0, 0), (281, 50, 1, 522 - 50))

    pygame.draw.rect(board, (0, 0, 0), (386, 50, 1, 522 - 50))
    pygame.draw.rect(board, (0, 0, 0), (437, 50, 1, 522 - 50))


useless_variable = 1  # to run solve function only once


def drawing_numbers_on_board():
    global num, clicked, printed_board, empty_board, blank_spaces, useless_variable
    # if solve button is clcked run solve function and display it, else display unsolved board
    if solve_butt():
        clicked = True
        printed_board = completed_board
    else:
        if not clicked and useless_variable == 1:
            printed_board = num

    ######################################################################################################
    font = pygame.font.SysFont('Comic Sans MS', 30)
    xna = 0
    yna = 0
    for y in range(9):
        if (y) % 3 == 0 or y == 0:
            yna += 4
        else:
            yna += 1
        for x in range(9):

            if (x) % 3 == 0 or x == 0:
                xna += 4
            else:
                xna += 1
            ###############################################
            x_text = 20 + (x * 50) + xna
            y_text = 50 + (y * 50) + yna

            if printed_board[y][x] != 0:
                text = font.render(str(printed_board[y][x]), False, (0, 0, 0))
                board.blit(text, (
                    (x_text + 50 // 2) - (text.get_width() // 2), (y_text + 50 // 2) - (text.get_height() // 2)))

            else:
                if useless_variable == 1:
                    input.append([num_inputs(x_text, y_text, ('')), y, x])
            ############################################################################################
            if x == 8:
                xna = 0
    useless_variable = 2
    #########################################################################################################


class num_inputs:
    def __init__(self, x, y, text, r=30, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.text = text
        self.r = r
        self.color = color
        self.return_text = ''
        self.clicked = False
        self.correct = 2
        self.waiting_variable = 0

    def buttons(self):
        global lives
        self.button_nam = button(self.color, self.x, self.y, 50, 50)
        if self.correct == 2:
            if self.clicked == True:
                self.color = (191, 143, 143)

            elif self.button_nam.isOver(pygame.mouse.get_pos()):
                self.color = (200, 200, 200)
            else:
                self.color = (255, 255, 255)
        elif self.correct == 0:
            self.color = (67, 210, 105)
            if self.waiting_variable != 20:
                self.waiting_variable += 1
            else:
                self.waiting_variable = 0
                return True
        else:
            self.color = (219, 43, 43)
            # show red color for some amount of time, than remove the text
            if self.waiting_variable != 20:
                self.waiting_variable += 1
            else:
                self.return_text = ''
                self.waiting_variable = 0
                lives += 1
        self.button_nam = button(self.color, self.x, self.y, 50, 50)
        self.button_nam.draw(board)

    def isClicked(self):
        global key_unicode, pressed_key
        if pygame.mouse.get_pressed()[0]:
            if self.button_nam.isOver(pygame.mouse.get_pos()):
                self.clicked = True
        if self.clicked:
            if pressed_key == pygame.K_RETURN:
                self.text = self.return_text
                self.clicked = False
                return self.text
            else:
                if key_unicode.isnumeric():
                    self.return_text = key_unicode
                    self.text = self.return_text
                    self.clicked = False
                key_unicode = ''

    def check_correct(self, y, x):
        global printed_board, input
        if self.return_text.isnumeric() and completed_board[y][x] == int(self.return_text):
            self.correct = 0
        elif self.return_text.isnumeric() and completed_board[y][x] != int(self.return_text):
            self.correct = 1
        else:
            self.correct = 2

    def display_user_input(self):
        x_hranica = self.x + 50
        font = pygame.font.SysFont('Comic Sans MS', self.r)
        rend = font.render(self.return_text, False, (0, 0, 0))
        board.blit(rend, ((((x_hranica - self.x) // 2) + self.x) -
                          (rend.get_width() // 2), self.y))


def input_blank():
    global curently_clicked, printed_board
    if not clicked:
        for i in range(len(input)):
            if input[i][0].buttons():
                printed_board[input[i][1]][input[i]
                                           [2]] = input[i][0].return_text
                input.pop(i)
                break

            input[i][0].isClicked()
            input[i][0].check_correct(input[i][1], input[i][2])

            # So only 1 bracket can be activated!1
            if input[i][0].clicked == True and input[i][0] not in curently_clicked:
                curently_clicked.append(input[i][0])
                if len(curently_clicked) >= 2:
                    curently_clicked[0].clicked = False
                    curently_clicked.pop(0)
            input[i][0].display_user_input()


def load_image_to_sudoku():

    path_img = ''
    # draw_button
    if load_img_button():
        # open file browser
        root = tkinter.Tk()
        root.withdraw()  # hide tkinter window

        currdir = os.getcwd()
        path_img = filedialog.askopenfilename(
            parent=root, initialdir=currdir, title='Please select a img', filetypes=[('Image files', '.jpg .png')])

        root.destroy()

    # process image and get sudoku board from it
    if len(path_img) > 0:
        img_processing(path_img)


countdown = 0


def load_img_button():
    global countdown
    load_img_button = button((147, 158, 202), 600, 150,
                             250, 50, text='Load image', r=40)

    if load_img_button.isOver(pygame.mouse.get_pos()):
        load_img_button.color = (164, 164, 164)

    else:
        load_img_button.color = (147, 158, 202)

    load_img_button.draw(board)

    if load_img_button.isclicked():
        if countdown == 0:
            countdown = 100
            return True
        # switch so button isnt perma clicked
        if countdown != 0:
            countdown -= 1
            return False
    else:
        # switch so button isnt perma clicked
        if countdown != 0:
            countdown -= 1
        return False


def solve_butt():
    solve_button = button((147, 158, 202), 600, 50,
                          250, 50, text='Solve', r=40)

    if solve_button.isOver(pygame.mouse.get_pos()):
        solve_button.color = (164, 164, 164)

    else:
        solve_button.color = (147, 158, 202)

    solve_button.draw(board)

    if solve_button.isclicked():
        return True
        print('UEAAAAA')
    else:
        return False


def change_board():
    global board_num
    next_button = button((147, 158, 202), 750, 450, 120, 50, 'skip', r=50)
    if next_button.isOver(pygame.mouse.get_pos()):
        next_button.color = (164, 164, 164)
    else:
        next_button.color = (147, 158, 202)

    next_button.draw(board)

    if next_button.isclicked():
        if board_num + 1 < len(levels):
            board_num = 0
        else:
            board_num += 1
        solve()


def gmae_over():
    a = 80
    board.blit(black_x, (40, 530))
    board.blit(black_x, (40 + a, 530))
    board.blit(black_x, (40 + 2 * a, 530))

    if lives >= 4:
        font = pygame.font.SysFont('Comic Sans MS', 30)

    for i in range(lives):
        board.blit(red_x, (40 + a * i, 530))


def display_game_window():
    board.fill((255, 255, 255))

    solve_butt()
    drawing_play_board()
    drawing_numbers_on_board()
    input_blank()
    change_board()
    gmae_over()
    load_image_to_sudoku()

    pygame.display.update()


# main looop#########################################################################################################
if __name__ == '__main__':

    lives = 0
    curently_clicked = []
    empty_board = []
    board_num = 0
    num = levels[0]
    solve()
    board = pygame.display.set_mode((1000, 600))
    clicked = False
    run = True
    blank_spaces = {}
    input = []

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                pressed_key = event.key
                key_unicode = event.unicode
            else:
                pressed_key = ''
                key_unicode = ''

        display_game_window()
    pygame.quit()
