import cv2
import numpy as np
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

fontC = ImageFont.truetype("./Font/platech.ttf", 14, 0);

def drawRectBox(image, rects, cons, reses):
    #for image, rect, addText in zip(images, rects, addTexts):
    for rect in rects:
        cv2.rectangle(image, (int(rect[0]), int(rect[1])), (int(rect[0] + rect[2]), int(rect[1] + rect[3])), (0,0, 255), 2, cv2.LINE_AA)
        cv2.rectangle(image, (int(rect[0]-1), int(rect[1])-16), (int(rect[0] + 115), int(rect[1])), (0, 0, 255), -1, cv2.LINE_AA)

    img = Image.fromarray(image)
    draw = ImageDraw.Draw(img)

    for rect, con, res in zip(rects, cons, reses):
        #draw.text((int(rect[0]+1), int(rect[1]-16)), addText.decode("utf-8"), (255, 255, 255), font=fontC)
        draw.text((int(rect[0]+1), int(rect[1]-16)), res+" "+str(round(con, 3)), (255, 255, 255), font=fontC)

    imagex = np.array(img)
    return imagex
