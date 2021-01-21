import numpy as np
import cv2

def wrapAffine():
    img = cv2.imread('images/transform.jpg')
    
    #numpy array초기화
    pts1 = np.float32([ [50, 50], [200, 50], [20, 200] ])
    pts2 = np.float32([ [70, 150], [220, 120], [150, 300] ])

    #좌표를 옮기는 행렬을 m에 반환한다.
    m = cv2.getAffineTransform(pts1, pts2)

    #반환된 행렬을 통해 좌표픽셀들을 좌표이동을 시킨다.
    result = cv2.warpAffine(img, m, (700, 600))  #숫자는 변환될 이미지의 사이즈.

    cv2.imshow('original', img)
    # cv2.namedWindow('Affine Transform', cv2.WINDOW_NORMAL)
    cv2.imshow('Affine Transform', result)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    wrapAffine()