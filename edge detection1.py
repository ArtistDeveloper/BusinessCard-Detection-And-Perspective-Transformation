import numpy as np
import cv2

def contour():
    #원본 이미지
    imgfile = 'images/contour.jpg'
    img = cv2.imread(imgfile)
    #흑백이미지
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #canney Detection 알고리즘
    edge = cv2.Canny(imgray, 100, 200)
    edge, contours, hierarchy  = cv2.findContours(edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.imshow('edge', edge)

    cv2.drawContours(img, contours, -1, (0, 255, 0), 1)
    cv2.imshow('Contour', img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    contour()
