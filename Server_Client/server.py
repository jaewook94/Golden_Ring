import argparse
import pickle
import os
import numpy as np
import pandas as pd
import threading
from time import sleep, time
from socket import *

flag = -1
islive = True

def get_motion_name(m_id):

    if m_id == 0:
        motion = 'up2down'
    elif m_id == 1:
        motion = 'right2left'
    elif m_id == 2:
        motion = 'left2right'
    elif m_id == 3:
        motion = 'clockwise'
    elif m_id == 4:
        motion = 'cClockwise'
    elif m_id == 5:
        motion = 'neutral'

    return motion

def isAllZero(line):
    for element in line:
        if float(element) != 0.0:
            return False

    return True

def android_send():

    androidPort = 22990
    androidSocket = socket(AF_INET, SOCK_STREAM)
    androidSocket.bind(('', androidPort))
    print ("Ready to Recive from Android")

    global flag
    global islive

    androidSocket.listen(3)
    while islive:
        conn, addr = androidSocket.accept()
        print ("connected from android")

        while True:
            msg = conn.recv(2048)

            if not msg:
                print ('android disconnnect!')
                break

            if flag == 1:
                conn.send(bytes('r2l\n', 'UTF-8'))
                print ("Previous Song\n")
            elif flag == 2:
                conn.send(bytes('l2r\n', 'UTF-8'))
                print ("Next Song\n")
            elif flag == 3:
                conn.send(bytes('cw\n', 'UTF-8'))
                print ("Vol Up\n")
            elif flag == 4:
                conn.send(bytes('ccw\n', 'UTF-8'))
                print ("Vol down\n")
            flag = -1
        conn.close()
    androidSocket.close()
    
if __name__ == '__main__':
    bundle = []

    with open('./model/CNN.txt', 'rb') as f:
        model = pickle.load(f)

    print ("Do")
    print ()

    try:
        serverPort = 32990
        serverSocket = socket(AF_INET, SOCK_DGRAM)
        serverSocket.bind(('', serverPort))
        print ("Ready to Recive from Raspberry pi")

        and_thread = threading.Thread(target=android_send)

        and_thread.start()

        isStart = False
        startTime = 0
        endTime = 0

        total = 0
        while True:
            msg, clientAddr = serverSocket.recvfrom(2048)

            if not msg:
                print ("disconnected from client")
                break

            line = pickle.loads(msg)

            if line[0] == 'IO':
                print ("I/O Error! Check Again!")
                continue
            if isAllZero(line):
                print ("Line Error! Check Again!")
                continue

            bundle.append(line)

            if total > 16:
                bundle.pop(0)
                wrapper = []
                wrapper.append(bundle)

                np_bundle = np.asarray(wrapper)
                np_bundle = np_bundle.reshape(np_bundle.shape[0], 17, 6, 1)
                pred = model.predict_proba(np_bundle)

                if max(pred[0]) > 0.9:
                    motion = get_motion_name(np.argmax(pred[0]))
                    print (motion, "| ", max(pred[0]))
                    if motion == 'up2down':
                        isStart = True
                        startTime = time()
                    if isStart == True:
                        endTime = time()
                        if endTime - startTime > 5:
                            isStart = False
                    if motion != 'up2down' and motion != 'neutral' and isStart == True:
                        print ("motion send: ", motion)
                        if motion == 'right2left':
                            flag = 1
                        elif motion == 'left2right':
                            flag = 2
                        elif motion == 'clockwise':
                            flag = 3
                        elif motion == 'cClockwise':
                            flag = 4
                        startTime = time()
                        print ()

                    bundle.clear()
                    total = 0

            else:
                total += 1

    except Exception as e:
        print ("Error:", e)

    finally:
        islive = False
        serverSocket.close()
