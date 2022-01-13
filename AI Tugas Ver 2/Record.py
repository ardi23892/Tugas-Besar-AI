import cv2,os
import time
import numpy as np
from PIL import Image

#Capture Webcam
cap = 0
video = cv2.VideoCapture(cap, cv2.CAP_DSHOW)
#Import Haar Cascade
FaceRecog = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#Input data mahasiswa (range ID 1-250 aja)
id=input('Masukan Student ID: ')
name=input('Masukan nama: ')
a=0
while True:
    a=a+1
    check, frame = video.read()
    #Ubah frame per frame ke Grayscale/Hitam putih
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face = FaceRecog.detectMultiScale(grayscale,1.3,5)
    #Bikin rectangle sekaligus capture frame by frame di save sebagai .jpg dengan format nama "ID.Nama.NomorDataset.jpg"
    for (x1,y1,x2,y2) in face:
        cv2.imwrite('Dataset/'+str(id)+'.'+str(name)+'.'+str(a)+'.jpg', grayscale[y1:y1+y2,x1:x1+x2])
        cv2.rectangle(frame, (x1,y1), (x1+x2,y1+y2),(0,200,0),2)
    #Show window buat Webcam
    cv2.imshow("Webcam", frame)
    #Capture upto 30 Frame
    if (a>29):
        break
cv2.destroyAllWindows()

#Manggil code untuk training
import Train