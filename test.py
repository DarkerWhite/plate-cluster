import cv2
from time import time
from hyperlpr_py3 import pipline

img = cv2.imread("./img.jpg")

for i in range(100):
    start = time()
    print(pipline.SimpleRecognizePlateByE2E(img))
    print("time ", time()-start)
