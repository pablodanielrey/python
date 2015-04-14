import cv2
import sys
import time

# sys.argv[1] rtsp://127.0.0.1/video.mp4

cam = cv2.VideoCapture(sys.argv[1])
s, img = cam.read()

fps = 7
fourcc = cv2.cv.CV_FOURCC('M','P','J','G')
out = cv2.VideoWriter('output.avi',-1,fps,(640,480))

while s:
  img = cv2.flip(img,0)

  date = time.strftime("%H:%M:%S %d/%m/%Y")
  cv2.putText(img,date,(10,100), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 1)

  cv2.imshow('frame',img )
  out.write(img)

  s, img = cam.read()

  key = cv2.waitKey(10)
  if key == 27:
    break


cam.release()
out.release()
print "Goodbye"
