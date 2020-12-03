import os
import random
import numpy as np
import pandas as pd
import pickle
import gc
import lightgbm as lgb
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, StratifiedKFold, KFold
from sklearn.metrics import accuracy_score, confusion_matrix

DATASET_PATH = '../dataset/'
#actions = ['cClockwise', 'clockwise', 'left2right', 'right2left', 'up2down']
actions = ['neutral']

for action in actions:
    all_data = []

    print ("Open", action, "!\n")

    for example in os.listdir(DATASET_PATH + action):
        
        # example == 1.txt
        # action == cClockwise
        
        with open(DATASET_PATH + action + '/' + example, 'rb') as f:
            data = pickle.load(f)
            all_data.append(np.array(data).flatten().reshape(1, -1))

    data_num = len(all_data)
    
    print ("Load finish:", data_num)
    
    # data to dict
    data_dict = {}
    for i, data in enumerate(all_data):
        data_dict[i] = data

    print ("Added to dict")

    # create empty dataframe
    columns = [i for i in range(102)]
    indices = [i for i in range(data_num)]
    df = pd.DataFrame(columns=columns, index=indices)

    print ("Make dataframe")

    for i in range(data_num):
        df.loc[i] = data_dict[i]

    print ("Added data to dataframe")

    df.to_csv('../dataset/{}.csv'.format(action), index=False)
    print ("Saved {}.csv".format(action))
    print ('---------------------------\n')
