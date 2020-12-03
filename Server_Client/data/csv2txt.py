import os
import pandas as pd
import pickle

root_dir = '../dataset/'

for csv in os.listdir(root_dir):
    motion = csv.split('.')[0]

    data = pd.read_csv(os.path.join(root_dir, csv))

    print (f"\nLoad {motion} !\n")

    motion_dir = os.path.join(root_dir, motion)
    
    os.mkdir(motion_dir + '/')

    for i in range(len(data)):
        line = data.loc[i, :]
        file_name = os.path.join(motion_dir, f'{i:05}.txt') 
        
        with open(file_name, 'wb') as f:
            for j in range(17):
                col = j*6
                record = [line[col + 0], line[col+1], line[col+2], line[col+3], line[col+4], line[col+5]]
                pickle.dump (record, f)

    print ("Finish!")
