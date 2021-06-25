
import numpy as np
import cv2
from collections import deque
import time
import speech_recognition as sr
#import PyAudio



colorIndex =-10
download =False
closed=True
import mediapipe as mp

hand=mp.solutions.hands
my_hand=hand.Hands(max_num_hands=1)
mpdraw=mp.solutions.drawing_utils
zoom=0

def setValues(x):
   print("")


# whitescreen summa
whitescreen =np.zeros((480 ,640 ,3) ) +255

path =[5877]
blue_index = 0
green_index = 0
red_index = 0
yellow_index = 0
erbp =[]
ergp =[]
eryp =[]
errep =[]


kernel = np.ones((5 ,5) ,np.uint8)





cap = cv2.VideoCapture(0)

bp =[]
yp =[]
rp =[]
gp =[]
eraser =[]
bpt=None
gpt=None
ypt=None
rpt=None
colors =[(255 ,0 ,0) ,(0 ,255 ,0) ,(0 ,0 ,255) ,(0 ,255 ,255)]
true =True
paint=True

center =(320 ,240)

while true:
    save = False

    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    u_hue = cv2.getTrackbarPos("Upper Hue", "Color detectors")
    u_saturation = cv2.getTrackbarPos("Upper Saturation", "Color detectors")
    u_value = cv2.getTrackbarPos("Upper Value", "Color detectors")
    l_hue = cv2.getTrackbarPos("Lower Hue", "Color detectors")
    l_saturation = cv2.getTrackbarPos("Lower Saturation", "Color detectors")
    l_value = cv2.getTrackbarPos("Lower Value", "Color detectors")
    Upper_hsv = np.array([u_hue ,u_saturation ,u_value])
    Lower_hsv = np.array([l_hue ,l_saturation ,l_value])
    frame = cv2.rectangle(frame, (75 ,449), (140 ,479), (122 ,122 ,122), -1)
    frame = cv2.rectangle(frame, (160 ,449), (255 ,479), colors[0], -1)
    frame = cv2.rectangle(frame, (275 ,449), (370 ,479), colors[1], -1)
    frame = cv2.rectangle(frame, (390 ,449), (485 ,479), colors[2], -1)
    frame = cv2.rectangle(frame, (505 ,449), (600 ,479), colors[3], -1)
    frame = cv2.rectangle(frame, (1 ,449), (60 ,479), (255 ,255 ,255), -1)
    frame =cv2.rectangle(frame ,(1 ,1) ,(50 ,30) ,(255 ,255 ,255) ,-1)
    frame =cv2.rectangle(frame ,(80 ,1) ,(130 ,30) ,(255 ,255 ,255) ,-1)
    frame=cv2.rectangle(frame,(160,1),(210,30),(255,255,255),-1)
    frame=cv2.rectangle(frame,(240,1),(290,30),(255,255,255),-1)





    frame =cv2.rectangle(frame ,(590 ,1) ,(639 ,30) ,(255 ,255 ,255) ,-1)
    frame =cv2.rectangle(frame ,(0 ,40) ,(639 ,445) ,(0 ,0 ,255))



    cv2.putText(frame, "CLEAR ", (80, 464), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "ERASER", (5, 464), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "BLUE", (185, 464), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "GREEN", (298, 464), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "RED", (420, 464), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "YELLOW", (520 ,464 ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150 ,150 ,150), 2, cv2.LINE_AA)
    cv2.putText(frame, "new", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0 ,0 ,0), 2, cv2.LINE_AA)
    cv2.putText(frame, "save", (90, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0 ,0 ,0), 2, cv2.LINE_AA)
    cv2.putText(frame, "mic", (170, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0 ,0 ,0), 2, cv2.LINE_AA)
    cv2.putText(frame, "X", (615, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0 ,0 ,0), 2, cv2.LINE_AA)



    img_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    res = my_hand.process(img_rgb)
    if res.multi_hand_landmarks:
        for one_hand in res.multi_hand_landmarks:
            wr_x = one_hand.landmark[8].x
            wr_y = one_hand.landmark[8].y
            w_x = one_hand.landmark[6].x
            w_y = one_hand.landmark[6].y
            hc_x = one_hand.landmark[0].x
            hc_y = one_hand.landmark[0].y
            dis8 = (wr_x - hc_x) ** 2 + (wr_y - hc_y) ** 2
            dis6 = (w_x - hc_x) ** 2 + (w_y - hc_y) ** 2
            if dis8 > dis6:
                closed = False
            else:
                closed = True

            center = (int(wr_x * 640), int(wr_y * 480))

            mpdraw.draw_landmarks(frame, one_hand, hand.HAND_CONNECTIONS)
        # frame=cv2.rectangle(frame,(160,1),(210,30),(255,255,255),-1)
        if 160 <= center[0] <= 209 and 2 <= center[1] <= 29:
            r=sr.Recognizer()
            try:
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, duration=0.2)
                    aud = r.listen(source,phrase_time_limit=1)
                    gc_translator=r.recognize_google(aud)
                    gc_translator=gc_translator.lower()






                    if "blue" in gc_translator.split():
                        colorIndex = 0

                    if "green" in gc_translator.split():
                        colorIndex = 1
                    elif "red" in gc_translator.split():
                        colorIndex = 2
                    elif "yellow" in gc_translator.split():
                        colorIndex = 3
                    elif "eraser" in gc_translator.split():
                        colorIndex = -1
                    elif "razor" in gc_translator.split():
                        colorIndex = -1
                    elif "close" in gc_translator.split():
                        break

            except Exception as exc:
                print("speech not dectected")
                print("check ur microphone")




            continue

        if center[1] >= 440:
            if (cv2.waitKey(1) & 0xFF == ord("u")) or 70 <= center[0] <= 140:

                if path != [] and path[0] == 0 and len(bp) > 0:
                    bp.pop(len(bp) - 1)
                elif path != [] and path[0] == 1 and len(gp) > 0:
                    gp.pop(len(gp) - 1)
                elif path != [] and path[0] == 2 and len(rp) > 0:
                    rp.pop(len(rp) - 1)
                elif path != [] and path[0] == 3 and len(yp) > 0:
                    yp.pop(len(yp) - 1)
                elif path != [] and path[0] == -1 and len(eraser) > 0:
                    er = eraser[-1]
                    for i in erbp:

                        dis = (er[0] - i[0]) ** 2 + (er[1] - i[1]) ** 2
                        if dis < 100:
                            bp.append(i)
                    for i in errep:
                        dis = (er[0] - i[0]) ** 2 + (er[1] - i[1]) ** 2
                        if dis < 100:
                            rp.append(i)
                    for i in eryp:
                        dis = (er[0] - i[0]) ** 2 + (er[1] - i[1]) ** 2
                        if dis < 100:
                            yp.append(i)
                    for i in ergp:
                        dis = (er[0] - i[0]) ** 2 + (er[1] - i[1]) ** 2
                        if dis < 100:
                            gp.append(i)
                    eraser.pop(-1)

                if path != []:
                    path.pop(0)

                colorIndex = -10



            elif 160 <= center[0] <= 255:
                colorIndex = 0

            elif 275 <= center[0] <= 370:
                colorIndex = 1
            elif 390 <= center[0] <= 485:
                colorIndex = 2
            elif 505 <= center[0] <= 600:
                colorIndex = 3

            elif 0 <= center[0] <= 50:
                colorIndex = -1

        elif 40 <= center[1] <= 445:

            if colorIndex == -1:
                eraser.append(center)
                path = [-1] + path
                if center == []:
                    break

                for i in bp:
                    if i == None:
                        continue

                    dis = (center[0] - i[0]) ** 2 + (center[1] - i[1]) ** 2
                    if dis < 100:
                        bp.remove(i)
                        erbp.append(i)
                for i in rp:
                    if i == None:
                        continue
                    dis = (center[0] - i[0]) ** 2 + (center[1] - i[1]) ** 2
                    if dis < 100:
                        rp.remove(i)
                        errep.append(i)
                for i in yp:
                    if i == None:
                        continue
                    dis = (center[0] - i[0]) ** 2 + (center[1] - i[1]) ** 2
                    if dis < 100:
                        yp.remove(i)
                        eryp.append(i)

                for i in gp:
                    if i == None:
                        continue
                    dis = (center[0] - i[0]) ** 2 + (center[1] - i[1]) ** 2
                    if dis < 100:
                        gp.remove(i)
                        ergp.append(i)
            elif colorIndex == 0:
                bpt = center
            elif colorIndex == 1:
                gpt = center
            elif colorIndex == 2:
                rpt = center
            elif colorIndex == 3:
                ypt = center

        elif center[1] < 40:
            if 1 <= center[0] <= 50:
                yp = []
                gp = []
                rp = []
                bp = []
                eraser = []
                path = []
                colorIndex = -10
            elif 590 < center[0]:
                true = False
                break
            elif 80 <= center[0] <= 130:
                save = True

        # Append the next deques when nothing is detected to avois messing up
    if len(bp) > 2:

        for v in range(len(bp)):
            cv2.circle(frame, bp[v], 5, (255, 0, 0), cv2.FILLED)
    if len(gp) > 2:
        for v in range(len(gp)):
            cv2.circle(frame, gp[v], 5, (0, 255, 0), cv2.FILLED)

    if len(rp) > 2:
        for v in range(len(rp)):
            cv2.circle(frame, rp[v], 5, (0, 0, 255), cv2.FILLED)

    if len(yp) > 2:
        for v in range(len(yp)):
            cv2.circle(frame, yp[v], 5, (0, 255, 255), cv2.FILLED)
    if 40 <= center[1] <= 445:
        if not closed:
            if colorIndex == 0:
                cv2.circle(frame, bpt, 5, (255, 0, 0), cv2.FILLED)
                bp.append(bpt)
                path = [0] + path

            elif colorIndex == 1:
                cv2.circle(frame, gpt, 5, (0, 255, 0), cv2.FILLED)
                gp.append(gpt)
                path = [1] + path

            elif colorIndex == 2:
                cv2.circle(frame, rpt, 5, (0, 0, 255), cv2.FILLED)
                rp.append(rpt)
                path = [2] + path
            elif colorIndex == 3:
                cv2.circle(frame, ypt, 5, (0, 255, 255), cv2.FILLED)
                yp.append(ypt)
                path = [3] + path
            if colorIndex in [0, 1, 2, 3, -1]:
                path = [colorIndex] + path

    if save:

        cv2.imwrite("project1.jpg", frame)
        time.sleep(3)
        continue


    cv2.imshow("Tracking", frame)

    # If the 'q' key is pressed then stop the application
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    if cv2.waitKey(1) & 0xFF == ord("s"):
        cv2.imwrite("project1.jpg", frame)
        time.sleep(3)
        continue
cap.release()
cv2.destroyAllWindows()

