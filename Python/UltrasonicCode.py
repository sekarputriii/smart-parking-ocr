import serial
import os
import time
from importlib import reload



Arduino_in = serial.Serial('COM10',9600)
Arduino_out = serial.Serial('COM6',9600)


def servo_in(x):
    Arduino_in.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = Arduino_in.readline()
    return data
    

def servo_out(x):
    Arduino_out.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = Arduino_out.readline()
    return data

while True:
    if( Arduino_in.inWaiting()>0):
        data = str(Arduino_in.readline())
        print(data)

        if 'in' in data:
            print('Pintu Masuk')
            # os.system('py ocrreader_in.py')

            # servoin = ocrreader_in.servoin
            import ocrreader_in
            # reload(ocrreader_in)
            servoin = ocrreader_in.servoin
            
            if (servoin == "on"):
                print("Palang Masuk Terbuka")
                servo_in("1")
                # time.sleep(30)
                break


        
    elif (Arduino_out.inWaiting()>0):
        data = str(Arduino_out.readline())
        print(data)

        if 'out' in data:
            print('Pintu Keluar')
            # os.system('py ocrreader_out.py') 

            import ocrreader_out
            # servoout = ocrreader_out.servoout
            # reload(ocrreader_out)
            servoout = ocrreader_out.servoout

            if (servoout == "on"):
                print("Palang Keluar Terbuka")
                servo_out("2")
                # time.sleep(30)
                break
                
            
        
