import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import os
import random
import sys
import tensorflow as tf
import keras
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers.convolutional import Conv2D, MaxPooling2D
import numpy as np
import pandas as pd
import pickle

np.random.seed(2990)

def get_dataframes():
    df1 = pd.read_csv('./dataset/cClockwise.csv')
    df2 = pd.read_csv('./dataset/clockwise.csv')
    df3 = pd.read_csv('./dataset/left2right.csv')
    df4 = pd.read_csv('./dataset/right2left.csv')
    df5 = pd.read_csv('./dataset/up2down.csv')
    df6 = pd.read_csv('./dataset/neutral.csv')

    df1['target'] = 4 # 반시계
    df2['target'] = 3 # 시계
    df3['target'] = 2 # 왼오
    df4['target'] = 1 # 오왼
    df5['target'] = 0 # 업다운
    df6['target'] = 5 # 중립

    data_num = len(df1) + len(df2) + len(df3) + len(df4) + len(df5) + len(df6)

    df = pd.DataFrame(columns=range(102), index=range(data_num))
    df = pd.concat([df1, df2], axis=0)
    df = pd.concat([df, df3], axis=0)
    df = pd.concat([df, df4], axis=0)
    df = pd.concat([df, df5], axis=0)
    df = pd.concat([df, df6], axis=0)

    df.append(df1)
    df.append(df2)
    df.append(df3)
    df.append(df4)
    df.append(df5)
    df.append(df6)

    return df

def train_test_split(df):
    df = df.sample(frac=1)
    
    train_num = int(len(df)*0.9)

    train_df = df[:train_num]
    test_df = df[train_num:]

    print ("Train Test Split Result: ")
    print ("Train_df shape:", train_df.shape, "  | Test_df shape:", test_df.shape)

    X_train = train_df.iloc[:, :-1]
    y_train = train_df['target']
    X_test = test_df.iloc[:, :-1]
    y_test = test_df['target']

    return X_train, y_train, X_test, y_test

def saveModel(model):
    with open('./model/CNN.txt', 'wb') as f:
        pickle.dump(model, f)

if __name__ == '__main__':
    data = get_dataframes()
    X_train, y_train, X_test, y_test = train_test_split(data)

    rows = 17
    cols = 6
    input_shape = (17, 6, 1)


    X_train = X_train.values
    X_test = X_test.values
    y_train = y_train.values
    y_test = y_test.values

    X_train = X_train.reshape(X_train.shape[0], rows, cols, 1)
    X_test = X_test.reshape(X_test.shape[0], rows, cols, 1)
    y_train = y_train.reshape(y_train.shape[0], 1)
    y_test = y_test.reshape(y_test.shape[0], 1)

    y_train = to_categorical(y_train)
    y_test = to_categorical(y_test)

    batch_size = 32
    num_classes = 6
    epochs = 70

    model = Sequential()
    model.add(Conv2D(32, kernel_size=(5,5), strides=(1, 1), padding='same', input_shape = input_shape, activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
    model.add(Conv2D(64, (2, 2), activation='relu', padding='same'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(1000, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='softmax'))
    model.summary()

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    hist = model.fit(X_train, y_train, batch_size=batch_size, epochs= epochs, verbose=1, validation_data =(X_test, y_test))

    score = model.evaluate(X_test, y_test, verbose=0)
    print ('Test loss:', score[0])
    print ('Test acc:', score[1])

    saveModel(model) 
