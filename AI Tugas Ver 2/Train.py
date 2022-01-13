import cv2, os
import numpy as np
from PIL import Image

#Delete file training.xml jika ada
if os.path.exists("Dataset/training.xml"):
  os.remove("Dataset/training.xml")

Recog = cv2.face.LBPHFaceRecognizer_create()
FaceDetect = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
#Proses Training
def getImagesWithLabels(path):
    #Ngambil nama file
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
    faceSamples=[]
    Ids=[]
    for imagePath in imagePaths:
        pilImage=Image.open(imagePath).convert('L')
        imageNp=np.array(pilImage,'uint8')
        #Ngambil ID dari nama file
        Id=int(os.path.split(imagePath)[-1].split(".")[0])
        faces=FaceDetect.detectMultiScale(imageNp)
        for (x1,y1,x2,y2) in faces:
            faceSamples.append(imageNp[y1:y1+y2,x1:x1+x2])
            Ids.append(Id)
    return faceSamples, Ids
faces, Ids = getImagesWithLabels('Dataset')
Recog.train(faces, np.array(Ids))
#Ngesave data training ke bentuk .xml
Recog.save('Dataset/training.xml')