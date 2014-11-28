import sys
import time
import cv2
import cv2.cv as cv
import time
from Queue import Queue
from threading import Thread
from os import walk


def getFiles(dir):
	f = []
	for (dirpath,dirnames,filenames) in walk(dir):
		for file in sorted(filenames):
			if ".jpg" in file:
				f.append(dirpath + "/" + file)
	return f;



fps = 7
fourcc = cv.CV_FOURCC('F','M','P','4')
out = cv2.VideoWriter('output.avi',fourcc,fps,(640,480))

for f in getFiles(sys.argv[1]):
	image = cv2.imread(f)
	out.write(image)
	

out.release()

exit(1)


def showImages(q):
	while True:
		if not q.empty():
			while not q.empty():
				image = q.get()
				cv2.imshow( winName, image)
			q.task_done()
	

images = Queue(maxsize=0)
#worker = Thread(target=showImages,args=(images,))
#worker.setDaemon(True)
#worker.start()


def diffImg(t0, t1, t2):
  d1 = cv2.absdiff(t2, t1)
  d2 = cv2.absdiff(t1, t0)
  return cv2.bitwise_and(d1, d2)

fps = int(cam.get(cv.CV_CAP_PROP_FPS))

winName = "Camera"
cv2.namedWindow(winName, cv2.CV_WINDOW_AUTOSIZE)

winName2 = "Movement Indicator"
cv2.namedWindow(winName2, cv2.CV_WINDOW_AUTOSIZE)

# Read three images first:
t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
image = cam.read()[1]

#t_minus = cam.read()[1]
#t = cam.read()[1]
#t_plus = cam.read()[1]


videos = 0
recording = False
count = 0
out = None

while True:


  date = time.strftime("%H:%M:%S %d/%m/%Y")
  cv2.putText(image,date,(10,100), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 1)


  # detecto el movimiento en base a cantidad de pixels cambiados.
  diffimg = diffImg(t_minus, t, t_plus)
  count = cv2.countNonZero(diffimg)
#  print("Movement index : " + str(count))
  
  if not recording and count > sys.argv[2]:
    print("iniciando grabacion")
    recording = True
    count = 0

  if recording and count == 0:
#    fourcc = cv.CV_FOURCC('V','P','8','0')
    count = count + 1
    
  if recording and count > 0:
    out.write(image)
    count = count + 1

  if recording and (count > (25 * 60 * 60)):
    print("finalizando grabacion")
    recording = False
    count = 0
    out.release()
    videos = videos + 1


# images.put(image)
  cv2.imshow( winName2, diffimg)

  cv2.imshow( winName, image)

  image = cam.read()[1]
  t_minus = t
  t = t_plus
  t_plus = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

#  showImages(images)

  key = cv2.waitKey(10)
  if key == 27:
    cv2.destroyWindow(winName)
    break

print "Goodbye"
