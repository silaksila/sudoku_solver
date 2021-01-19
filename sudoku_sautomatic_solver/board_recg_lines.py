import cv2
import numpy as np
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


img = cv2.imread('imgs/sudoku_screen.png', 0)
# processing image
img = cv2.GaussianBlur(img, (7, 7), 0)
img = cv2.adaptiveThreshold(
    img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
edges = cv2.Canny(img, 5, 100)

# find lines in sudoku
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 10,
                        minLineLength=30, maxLineGap=10)
# remove lines from sudoku
for i in range(len(lines)):
    for x1, y1, x2, y2 in lines[i]:
        cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 4)

# run OCR for every square in sudoku:
img_height, img_weight = img.shape
custom_config = r'--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'
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

for y in range(9):
    for x in range(9):
        # square is a section of photo with only 1 number shown
        square = img[y*(img_height//9):(y+1)*(img_height//9),
                     x*(img_weight//9):(x+1)*(img_weight//9)]

        num = pytesseract.image_to_string(square, config=custom_config)
        num = re.findall('\d+', num)
        if num:
            board[y][x] = int(num[0])


showed_img = img[8*(img_height//9):(img_height//9)*9, 8 *
                 (img_weight//9):9*(img_weight//9)]

cv2.imshow("org", img)
cv2.waitKey(0)
