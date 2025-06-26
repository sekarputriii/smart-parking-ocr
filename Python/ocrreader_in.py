import cv2 
import csv
import pytesseract
import imutils
import glob
import os
import re
import pandas as pd
import numpy as np
from datetime import datetime
import time

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
path = r"D:\File Kuliah\Skripsi\Fix Beneran Fix\images-in"

# Get Jam Masuk 
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

# Database Kendaraan
vehicle = pd.read_csv("Database/Database_Kendaraan.csv")
df = pd.DataFrame(vehicle)

# Get Image 
cap = cv2.VideoCapture(2)
frame_set = []
start_time = time.time()

if (cap.isOpened()==False):
    print('Error Reading video')

while True:
    ret,frame = cap.read()
    cv2.imshow("Pintu Masuk", frame)
    files = next(os.walk(path))[2] 
    counts = len(files) + 1

    # Image Processing
    img = imutils.resize(frame)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray1 = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(gray, 30, 200)

    # Contour
    (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]

    NumberPlateCnt = None

    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            NumberPlateCnt = approx
            img2 = img.copy()
            contours = cv2.drawContours(img2, [NumberPlateCnt], -1, (0,255,0), 3)
            x, y, w, h = cv2.boundingRect(c)
            plate = img [ y: y + h, x: x + w]
            break
        else:
            plate = frame
            break

    # Binerization
    plate = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, count = cv2.threshold(plate, 125, 255, cv2.THRESH_BINARY)

    black = np.sum(count == 0)
    white = np.sum(count == 255)

    if(black > white):
        th, thres = cv2.threshold(plate, 100, 192, cv2.THRESH_BINARY)
    else:
        th, thres = cv2.threshold(plate, 80, 192, cv2.THRESH_BINARY_INV)

    # time.sleep(3)
    text = pytesseract.image_to_string(thres, config='--psm 11')
    license = text.split("\n")[0]
    result = re.sub(r'\s+', '',   license)
    print(result)

    df2 = df.query("Plat == @result")
    if not df2.empty:
        img_name = "_{}.png".format(counts)
        cv2.imwrite(path+ "\img" + img_name, frame)
        # print("img" + img_name + ' written!'.format(counts))
        start_time = time.time()
        count += 1
        print("Kendaraan Terdaftar")
        servoin = "on"
        with open("Database/Database_Parkir.csv", 'a', newline='') as parkir:
            writer = csv.writer(parkir)
            writer.writerow([result, dt_string])
        parkir.close()
        cv2.destroyWindow("Pintu Masuk")
        break
    elif cv2.waitKey(1) & 0xFF == ord('q'):
        break
    else:
        print("Plat Tidak Terdaftar")
        servoin = "off"
            
