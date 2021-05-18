# import cv2
import sys
import time
import json
import struct
import socket
from base64 import b64decode
from hyperlpr_py3 import pipline

from common import device, bufferSize, printT, getData

def analyzeImage(img):
    res = json.dumps(pipline.SimpleRecognizePlateByE2E(img)).encode()
    return res

# server main below
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
    serversocket.bind(device['wsl'])
    serversocket.settimeout(3.0)
    serversocket.listen(0)  # max listen num: only listen one connection to avoid data seperation

    print('\033c')
    printT(f"Listening to {device['wsl']}.")
    while True:
        try:
            try:
                clientsocket, addr = serversocket.accept()
            except socket.timeout:
                continue
            printT(f"Client addr: {addr}")

            data = getData(clientsocket)
            printT(f"Received data length: {len(data)}")

            printT("Analyzeing image.")
            plateResult = analyzeImage(data)

            printT(f"Sending back result length: {len(plateResult)}")
            clientsocket.sendall(plateResult)
            clientsocket.close()
            printT(f"Listening to {device['wsl']}.")

        except socket.timeout:
            printT("Error: Connection timeout.")
        except KeyboardInterrupt:
            printT("Server terminated by user.")
            break
