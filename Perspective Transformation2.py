import numpy as np
import cv2

def warpPerspective():
    img = cv2.imread('images/transform2.jpg')

    #기존의 외곽검출을 통해서 네 개의 꼭지점을 찾았다고 가정. 원본 이미지의 네 개의 꼭지점을 나타냄.
    tooLeft = [104, 116]
    tooRight = [393, 118]
    bottomRight = [480, 520]
    bottomLeft = [12, 520]

    pts1 = np.float32([tooLeft, tooRight, bottomRight, bottomLeft])

    #네 개의 좌표를 이용해서 두 개의 너비, 두 개의 높이를 구한다.
    w1 = abs(bottomRight[0] - bottomLeft[0])
    w2 = abs(tooRight[0] - tooLeft[0])
    h1 = abs(tooRight[1] - bottomRight[1])
    h2 = abs(tooLeft[1] - bottomLeft[1])
    minWidth = min([w1, w2])
    minHeight = min([h1, h2])

    pts2 = np.float32([ [0,0], [minWidth-1, 0], [minWidth-1, minHeight-1], [0, minHeight-1] ])

    n = cv2.getPerspectiveTransform(pts1, pts2)

    result = cv2.warpPerspective(img, n, (int(minWidth), int(minHeight)))

    cv2.imshow('original', img)
    cv2.imshow('Warp Transfrom', result)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    warpPerspective()