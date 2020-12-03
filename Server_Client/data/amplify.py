import os
import pickle
import operator
import numpy as np
from random import uniform, randint

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

            add_two_list(avg_list, original_data)

        divide_list(avg_list, len(files))

        print ("Calculated average of", action, "!\n")

        # amplify
        # Step 1. add noise for 5 times
        # Step 2. shift data

        # Step 1. add noise for 5 times
        for repeat in range(5):
            for record in files:
                noise = make_noise_list() 

                with open(DATASET_PATH + action + '/' + record, 'rb') as f:
                    noise_data = pickle.load(f)

                for idx, line in enumerate(noise_data):
                    noise_data[idx] = list(map(float, line))

                add_two_list(noise_data, noise)
                
                # Step 2. shift data

                # case 0: shift left, repeat 2 times
                log = list()

                for i in range(2):
                    cnt = 0
                    temp_noise = make_noise_list()
                    noise_avg = list()
                    
                    while True:
                        cnt = randint(1, 3)

                        if cnt not in log:
                            log.append(cnt)
                            break

                    new_data = noise_data[cnt:]

                    for j in range(cnt):
                        one_line = list()
                        for k in range(6):
                            one_line.append(avg_list[j-cnt][k] + temp_noise[j-cnt][k])
                        noise_avg.append(one_line)
                    new_data.extend(noise_avg)

                    # Save
                    new_name = DATASET_PATH + action + '/' + str(origin_cnt + amplify_cnt) + '.txt'
                    
                    with open(new_name, 'wb') as f:
                        pickle.dump(new_data, f)
                    
                    amplify_cnt += 1

                # case 1: shift right, repeat 2 times
                log = list()

                for i in range(2):
                    cnt = 0
                    temp_noise = make_noise_list()
                    noise_avg = list()

                    while True:
                        cnt = randint(1, 3)

                        if cnt not in log:
                            log.append(cnt)
                            break

                    new_data = noise_data[:-cnt]

                    for j in range(cnt):
                        one_line = list()
                        for k in range(6):
                            one_line.append(avg_list[j][k] + temp_noise[j][k])
                        noise_avg.append(one_line)
                    new_data.extend(noise_avg)

                    # Save
                    new_name = DATASET_PATH + action + '/' + str(origin_cnt + amplify_cnt) + '.txt'
                    
                    with open(new_name, 'wb') as f:
                        pickle.dump(new_data, f)
                    
                    amplify_cnt += 1

        print (action, "finished!")
        print ("Befor:", origin_cnt, " |  After:", amplify_cnt + origin_cnt)
        print ("\n-------------------------------\n")


