import cv2
from csv import writer
import pytesseract
import imutils
import glob
import os
import re
import pandas as pd
from datetime import datetime
import numpy as np
import time

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
path = r"D:\File Kuliah\Skripsi\Fix Beneran Fix\images-out"

# Get Jam Keluar 
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

# Database parkir
vehicle = pd.read_csv("Database/Database_Parkir.csv")
df = pd.DataFrame(vehicle)

# Get Image 
cap = cv2.VideoCapture(1)
frame_set = []
start_time = time.time()

if (cap.isOpened()==False):
    print('Error Reading video')

while True:
    ret,frame = cap.read()
    cv2.imshow("Pintu Keluar", frame)
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
            plate = img
            break

    # Binerization
    plate = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
    ret, count = cv2.threshold(plate, 125, 255, cv2.THRESH_BINARY)

    black = np.sum(count == 0)
    white = np.sum(count == 255)

    # print(black)
    # print(white)

    if(black > white):
        th, thres = cv2.threshold(plate, 100, 192, cv2.THRESH_BINARY)
        # kernel = (5,5)
        # thres = cv2.morphologyEx(thres, cv2.MORPH_OPEN, kernel)
    else:
        th, thres = cv2.threshold(plate, 80, 192, cv2.THRESH_BINARY_INV)

    # cv2.imshow("Plat Kendaraan", thres)
    # cv2.waitKey()

    text = pytesseract.image_to_string(thres, config='--psm 11')
    license = text.split("\n")[0]
    result = re.sub(r'\s+', '',   license)
    print(result)

    df2 = df.query("Kendaraan == @result")
    # df3 = df.query("Jam Keluar")

    if not df2.empty:
        img_name = "_{}.png".format(counts)
        cv2.imwrite(path+ "\img" + img_name, frame)
        # print("img" + img_name + ' written!'.format(counts))
        start_time = time.time()
        count += 1
        print("Silahkan Keluar")
        servoout = "on"
        updated = df['Kendaraan'] == result
        check = df['Jam Keluar'].isna()
        # df.loc[updated, 'Jam Keluar'] = dt_string
        df['Jam Keluar'] = np.where(updated & check, dt_string, df['Jam Keluar'])
        df.to_csv('Database/Database_Parkir.csv', index=False)
        print(df)
        break
    elif cv2.waitKey(1) & 0xFF == ord('q'):
        break
    else:
        servoout = "off"
        print("Kendaraan Tidak Terdaftar")
                
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
