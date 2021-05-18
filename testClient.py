import cv2
from time import time
from time import sleep
from common import device
from client import sendImg

img = cv2.imread('./img.jpg')
for i in range(200):
    start = time()
    print(sendImg(device['wsl'], img))
    print(f"total time {time()-start}")
    print()
