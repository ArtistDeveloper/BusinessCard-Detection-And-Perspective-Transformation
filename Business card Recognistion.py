import numpy as np
import cv2

def order_points(pts):
    rect = np.zeros((4,2 ), dtype='float32')

    s= pts.sum(axis = 1)

    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect

def auto_scan_image():
    #명함 이미지 가져오기
    image = cv2.imread('images/document2.jpg')
    orig = image.copy()

    r = 800.0 / image.shape[0]
    dim = (int(image.shape[1] * r), 800)
    image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    edged = cv2.Canny(gray, 75, 200)

    print("STEP 1: Edge Detection")

    cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Edged', cv2.WINDOW_NORMAL)
    cv2.imshow("Image", image)
    cv2.imshow("Edged", edged)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    (_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]

    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        #임시방편으로 쓴 방법
        # print(len(approx))

        # if len(approx) == 8:
        #     screenCnt = approx
        #     break

        #조건문이 동작하지 않아 screenCnt에 값이 들어가지 않고 에러가 남.
        #+@ 문제는 해결했음. 문제였던 것은 document 이미지의 책상을 보면 길쭉한 선이 많이 나오는데, 
        # 책상이 매끈하지 않았기에, 꼭지점을 4개로 찾아내지 못했던 것임. document에서는 최소 꼭짓점이 8개 나왔음.
        if len(approx) == 4:
            print('hihi')
            screenCnt = approx
            break

    print("STEP 2: Find Contours of Paper")

    cv2.drawContours(image, [approx], -1, (0, 255, 0), 2)
    cv2.imshow("Outline", image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.waitKey(1)

    rect = order_points(screenCnt.reshape(4, 2) / r)
    (tooLeft, tooRight, bottomRight, bottomLeft) = rect

    w1 = abs(bottomRight[0] - bottomLeft[0])
    w2 = abs(tooRight[0] - tooLeft[0])
    h1 = abs(tooRight[1] - bottomRight[1])
    h2 = abs(tooLeft[1] - bottomLeft[1])

    maxWidth = max([w1, w2])
    maxHeight = max([h1, h2])

    dst = np.float32([ [0, 0], [maxWidth-1, 0], [maxWidth-1, maxHeight-1], [0, maxHeight-1] ])

    n = cv2.getPerspectiveTransform(rect, dst)

    warped = cv2.warpPerspective(orig, n, (maxWidth, maxHeight))

    print('STEP# : Apply perspective transform')
    cv2.imshow("Warped", warped)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.waitKey(1)

    warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)

    warped = cv2.adaptiveThreshold(warped, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 10)

    print("STEP 4 : Apply Adaptive Threshold")
    cv2.imshow('Original', orig)
    cv2.imshow("Scanned", warped)
    cv2.imwrite("scannedimage.png", warped)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    auto_scan_image()
