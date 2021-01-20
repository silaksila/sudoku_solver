import cv2
import numpy as np
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

custom_tesseract_config = r'--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'

board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

comare_compare = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# this function process image nad return board


def img_processing(path):
    img = cv2.imread(path, 0)
    # processing image
    img = cv2.resize(img, (900, 900))
    img = cv2.adaptiveThreshold(
        img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)
    edges = cv2.Canny(img, 100, 400)

    # find lines in sudoku
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100,
                            minLineLength=100, maxLineGap=30)
    # remove lines from sudoku
    #example = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    for i in range(len(lines)):
        for x1, y1, x2, y2 in lines[i]:
            #cv2.line(example, (x1, y1), (x2, y2), (0, 255, 0), 12)
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 12)

    img = cv2.GaussianBlur(img, (9, 9), 0)

    # run OCR for every square in sudoku:
    img_height, img_weight = img.shape
    for y in range(9):
        for x in range(9):
            # square is a section of photo with only 1 number shown
            square = img[y*(img_height//9):(y+1)*(img_height//9),
                         x*(img_weight//9):(x+1)*(img_weight//9)]

            num = pytesseract.image_to_string(
                square, config=custom_tesseract_config)
            num = re.findall('\d+', num)
            if num:
                board[y][x] = int(num[0])

    # img = img[0*(img_height//9):(1)*(img_height//9),
     #         0*(img_weight//9):(1)*(img_weight//9)]

    cv2.imwrite('imgs/test.png', img)
    cv2.imshow('aa', edges)
    cv2.waitKey(0)

    if board != comare_compare:
        print(board)
        return board
    else:
        print('BAD')
        return False


img_processing('imgs/sudoku_screen.png')
