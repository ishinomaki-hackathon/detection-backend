import cv2
import time
import numpy as np
import math
from handtrackingmodule import handDetector
import osascript





#################################
wCam, hCam = 640, 480
volume = 0
volume_bar = 400

#################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
detector = handDetector()

while True:
    success, img = cap.read()
    detector.findHands(img)
    lmlist = detector.findPosition(img, draw=False)

    if len(lmlist) != 0:
        # print(lmlist[4], lmlist[8])

        x1, y1 = lmlist[4][1], lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2


        cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        print(length)

        volume = np.interp(length,[13, 180], [0, 100])
        volume_bar = np.interp(length, [13, 180], [400, 150])
        print(volume)

        vol = "set volume output volume " + str(volume)
        osascript.osascript(vol)

        if length < 50:
            cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)

    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (50, int(volume_bar)), (85, 400), (0, 255, 0), cv2.FILLED)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (50, 70), cv2.FONT_HERSHEY_COMPLEX, 1,(255, 0, 0), 2)

    cv2.imshow('Img', img)
    cv2.waitKey(1)