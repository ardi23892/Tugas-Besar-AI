import cv2,os
from datetime import datetime, time, date
from openpyxl import Workbook, load_workbook
from PIL import Image

def time_in_range(start, end, current):
    return start <= current <= end

start = time(6,30,0)
end = time(12, 00, 0)

#Import Excel
wb = load_workbook('Attendance.xlsx')

#Import sheet excel
checkin = wb['Checkin']
checkout = wb['Checkout']

#Bikin list baru buat data check in
in_checked=[]
out_checked=[]

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
        #Find ID dari muka
        id, conf = Recog.predict(grayscale[y1:y1+y2,x1:x1+x2])

        #Import current time buat nentuin check in atau check out
        current = datetime.now().time()
        if(time_in_range(start, end, current)):
            #Cek sebelumnya sudah check-in atau belum
            if id not in in_checked:
             #Masukin ID ke list in_checked supaya ga check-in terus"an
                in_checked.append(id)
                #Ngambil time buat di print ke excel
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                #Cari last row buat formula vlookup
                LastRow = checkin.max_row +1
                #Append data ke excel
                checkin.append([id,'=VLOOKUP(A'+str(LastRow)+',\'Namelist\'!A:B,2,FALSE)',date.today(),current_time])
                
                #Save file excel
                wb.save('Attendance.xlsx')
        else:
            #Cek sebelumnya sudah check-out atau belum
            if id not in out_checked:
             #Masukin ID ke list in_checked supaya ga check-out terus"an
                out_checked.append(id)
                #Ngambil time buat di print ke excel
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                #Cari last row buat formula vlookup
                LastRow = checkout.max_row +1
                #Append data ke excel
                checkout.append([id,'=VLOOKUP(A'+str(LastRow)+',\'Namelist\'!A:B,2,FALSE)',date.today(),current_time])
                
                #Save file excel
                wb.save('Attendance.xlsx')
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
