import cv2
import numpy as np 
from matplotlib import pyplot as plt 

img = cv2.imread('./projectData/normal/26939_000_OK.jpeg',0)
blur = cv2.GaussianBlur(img,(5,5),0)

ret1, th1 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
ret2, th2 = cv2.threshold(img, 190, 255, cv2.THRESH_BINARY)

cv2.imshow("img", img)
cv2.imshow("th1", th1)
cv2.imshow("th2", th2)

cv2.waitKey(0)
cv2.destroyAllWindows() # 모든 창 닫기
cv2.waitKey(1)