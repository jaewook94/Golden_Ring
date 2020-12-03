import smbus			#import SMBus module of I2C
from time import sleep          #import
from datetime import datetime
import argparse
import pickle
import os
import sys

#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47

bus = smbus.SMBus(1)
# or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address

def MPU_Init():
    #write to sample rate register
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
    #Write to power management register
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	
    #Write to Configuration register
    bus.write_byte_data(Device_Address, CONFIG, 0)
	
    #Write to Gyro configuration register
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
	
    #Write to interrupt enable register
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)
    print ("Initalized GPIO!")
    print ()


def read_raw_data(addr):
    #Accelero and Gyro value are 16-bit
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr+1)
    
    #concatenate higher and lower value
    value = ((high << 8) | low)
        
    #to get signed value from mpu6050
    if(value > 32768):
        value = value - 65536
    return value


def record():
	
    #Read Accelerometer raw value
    acc_x = read_raw_data(ACCEL_XOUT_H)
    acc_y = read_raw_data(ACCEL_YOUT_H)
    acc_z = read_raw_data(ACCEL_ZOUT_H)
	
    #Read Gyroscope raw value
    gyro_x = read_raw_data(GYRO_XOUT_H)
    gyro_y = read_raw_data(GYRO_YOUT_H)
    gyro_z = read_raw_data(GYRO_ZOUT_H)
	
    #Full scale range +/- 250 degree/C as per sensitivity scale factor
    Ax = acc_x/16384.0
    Ay = acc_y/16384.0
    Az = acc_z/16384.0
	
    Gx = gyro_x/131.0
    Gy = gyro_y/131.0
    Gz = gyro_z/131.0

    record = [str(round(Gx,4)),  str(round(Gy,4)), str(round(Gz,4)),  str(round(Ax,4)), str(round(Ay,4)), str(round(Az, 4))]

    print (record)
    sleep(0.05)
    return record

def get_motion_name():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=int,help="0: up2down, 1: right2left, 2: left2right, 3: clockwise, 4: cClockwise 5: Neutral", choices=[0,1,2,3,4,5], metavar='Motion_id', required=True) 
    
    args = parser.parse_args()

    m_id = args.i
    motion = ""

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

def isExistDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def isAllZero(line):
    for element in line:
        if float(element) != 0.0:
            return False

    return True
    
if __name__ == '__main__':
    MPU_Init()
    
    motion = get_motion_name()
    result_path = '../dataset/' + motion + '/'
    isExistDir(result_path)
    isFileOpen = False

    cnt = len(os.listdir(result_path))
   
    print ("current data in", str(result_path), ": ", cnt)

    try:
        while True:

            c = input("input 's' or else ('r' to refresh): ")

            if('s' == c):
                bundle = []
                total = 0
                isError = False

                while total < 17:
                    line = record()
                    if isAllZero(line):
                        print ("Line Error! Ignored!")
                        isError = True
                        break
                    bundle.append(line)
                    total += 1

                    f_name = result_path + str(cnt) + '.txt'

                    if not isError:
                        isFileOpen = True
                        with open(f_name, 'wb') as f:
                            pickle.dump(bundle, f)
                        isFileOpen = False
                        print (f_name + " saved!!")
                        print ()
                
            elif('r' == c):
                cnt = len(os.listdir(result_path))
                print ("Current data in", str(result_path), ": ", cnt)

            else:
                break

            cnt += 1
    except Exception as e:
        print (e)

        if isFileOpen:
            cnt = len(os.listdir(result_path))
            cnt -= 1
            print (str(cnt) , ".txt removed!")
            remove(result_path + str(cnt)) + '.txt'
