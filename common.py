import cv2
import time
import json
import struct
import numpy as np

bufferSize = 2048

device = {
    'wsl': ('172.26.24.32', 5000),
    'cam-node-1': ('169.254.157.19', 5000)
}

def getTime():
    return time.strftime("%Y-%m-%d %X")

def printT(text):
    print(f"[{getTime()}]: {text}")

def getJson(socket):
    # get json file
    jsonLength = struct.unpack(">I", socket.recv(4))[0]
    printT(f"Json length: {jsonLength}")
    jsonData = b""
    while len(jsonData) < jsonLength:
        data = socket.recv(min(bufferSize, jsonLength - len(jsonData)))
        if not data:
            printT("Error: receive data error.")
            return -1
            break
        jsonData += data
    jsonData = json.loads(jsonData.decode("utf-8"))
    return jsonData

def getData(socket):
    dataLength = struct.unpack(">I", socket.recv(4))[0]
    printT(f"Data length: {dataLength}")
    imgData = b""
    while len(imgData) < dataLength:
        data = socket.recv(min(bufferSize, dataLength - len(imgData)))
        if not data:
            printT("Error: receive data error.")
            return -1
        imgData += data
    imgData = np.frombuffer(imgData, dtype=np.uint8)
    imgData = cv2.imdecode(imgData, cv2.IMREAD_COLOR)
    return imgData
