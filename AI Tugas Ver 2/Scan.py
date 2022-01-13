import cv2,os
import time
from PIL import Image

#Jika belum ada data muka yang dimasukan, jalankan Record.py dahulu!!

#Capture Webcam
cap = 0
video = cv2.VideoCapture(cap, cv2.CAP_DSHOW)

#Import Haar Cascade
FaceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#Read .xml dari training data
Recog = cv2.face.LBPHFaceRecognizer_create()
Recog.read('Dataset/training.xml')
a=0
while True:
    a=a+1
    check, frame = video.read()
    #Ubah frame per frame ke Grayscale/Hitam putih
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face = FaceDetect.detectMultiScale(grayscale,1.3,5)
    #Bikin rectangle dan ID di sekitar muka
    for (x1,y1,x2,y2) in face:
        cv2.rectangle(frame, (x1,y1), (x1+x2,y1+y2),(0,200,0),2)
        id, conf = Recog.predict(grayscale[y1:y1+y2,x1:x1+x2])
        cv2.putText(frame,str(id),(x1+10,y1-10), cv2.FONT_HERSHEY_DUPLEX, 1, (0,200,0),2)
    #Show window buat webcam
    cv2.imshow("Webcam", frame)
    #Waitkey 1 supaya video ga freeze
    key = cv2.waitKey(1)
    #Klik spasi jika ingin end program
    if key == ord(' '):
        break
    #Klik r jika ingin daftar wajah baru
    elif key== ord('r'):
        cv2.destroyAllWindows()
        import Record
        Recog = cv2.face.LBPHFaceRecognizer_create()
        Recog.read('Dataset/training.xml')
cv2.destroyAllWindows()
video.release()
