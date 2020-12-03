import os
import pickle
import operator
import sys
import numpy as np
from random import uniform, randint

write = sys.stdout.write

def make_empty_list(val=0.0):
    empty = list()

    for line in range(17):
        r = [val, val, val, val, val, val]
        empty.append(r)

    return empty

def make_noise_list(t=0.08):
    empty = list()

    for line in range(17):
        r = [uniform(-t, t), uniform(-t, t), uniform(-t, t), uniform(-t, t), uniform(-t, t), uniform(-t, t)]
        empty.append(r)

    return empty

def add_two_list(src, dst):
    for i in range(17):
        for j in range(6):
            src[i][j] += dst[i][j]

def divide_list(src, val):
    for i in range(17):
        for j in range(6):
            src[i][j] /= val

if __name__ == '__main__':
    DATASET_PATH = '../dataset/'
    actions = ['cClockwise', 'clockwise', 'left2right', 'right2left', 'up2down']

    for action in actions:
        print ("Open", action, "!")

        files = os.listdir(DATASET_PATH + action)

        avg_list = make_empty_list()
        origin_cnt = len(files)
        amplify_cnt = 0

        # get average of data
        for record in files:
            with open(DATASET_PATH + action + '/' + record, 'rb') as f:
                original_data = pickle.load(f)

            for idx, line in enumerate(original_data):
                original_data[idx] = list(map(float, line))

            test = np.asarray(original_data)

            if test.shape != (17, 6):
                print ("Error:", test.shape)
                print ("From", record)
                print ("----------------------------\n")

        print ("End", action)
        print ("------------------------------------\n")

 
