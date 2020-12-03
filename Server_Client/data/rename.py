import argparse
import pickle
import os
import numpy as np

   
if __name__ == '__main__':
    
    result_path = '../dataset/right2left/'

    files = os.listdir(result_path)
   
    print ("current data in", str(result_path), ": ", len(files))
    
    cnt = 0
    for f in files:
        os.rename(result_path + f, result_path + str(cnt) + '.txt')
        cnt += 1
