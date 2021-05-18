import cv2
import time
import json
import struct
import numpy as np

bufferSize = 2048

device = {
        'server': ('0.0.0.0', 5000),
        'proxy': ('169.254.237.196', 5000),
        'comp-node-1-fo': ('169.254.116.42', 5000),
        'comp-node-1-lo': ('172.26.24.32', 5000),
        'came-node-1': ('169.254.157.19'),
        'came-node-2': ('169.254.23.7'),
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
