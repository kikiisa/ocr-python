import cv2
from PIL import Image
import pytesseract
from Utils_NumberPlateRecognition import check1Line, corrrectCity, correctCapital, checkCity, checkOddEven, correctNumber, showText
import Utils
import easyocr
reader = easyocr.Reader(['en'])
numberPlatePoints = []
heightNumberPlate = 250

pytesseract.pytesseract.tesseract_cmd
pytesseract.pytesseract.tesseract_cmd = r'C:\\Tesseract-OCR\\tesseract.exe'
import numpy as np
import main
harcascade = "model/haarcascade_russian_plate_number.xml"

cap = cv2.VideoCapture("video/sample3.mp4")

cap.set(3, 640) # width
cap.set(4, 480) #height

min_area = 500

count = 0

while True:
    success, img = cap.read()

    plate_cascade = cv2.CascadeClassifier(harcascade)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)

    for (x,y,w,h) in plates:
        area = w * h

        if area > min_area:
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
            cv2.putText(img, "Number Plate", (x,y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)

            img_roi = img[y: y+h, x:x+w]
            cv2.imshow("ROI", img_roi)
            cv2.imwrite("images/scaned_img_" + str(count) + ".jpg", img_roi)
            
            img = cv2.imread(img_roi)
            scale = round(heightNumberPlate / img.shape[0], 1)
            img = Utils.resize(img, scale)
            detail = reader.readtext(img)
            numberPlate, datePlate = check1Line(img, detail) 
            print(numberPlate)

    cv2.imshow("Result", img)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        names = "plates/scaned_img_" + str(count) + ".jpg"
        cv2.imwrite(names, img_roi)

        img1 = np.array(Image.open(names))
        cv2.rectangle(img, (0,200), (640,300), (0,255,0), cv2.FILLED)
        cv2.putText(img, "Plate Saved", (150, 265), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255), 2)
        cv2.imshow("Results",img)
        cv2.waitKey(500)
        count += 1

