import  cv2
import mediapipe as mp
from collections import deque
import  time
from random import randint
s=0
import speech_recognition as sr
cap=cv2.VideoCapture(0)
hand=mp.solutions.hands
my_hand=hand.Hands(max_num_hands=1)
mpdraw=mp.solutions.drawing_utils
t=0
wait=False
first_innings=True

closed=True
choose=False
prev_no=deque([0,0,0,0,0],maxlen=10)
close_open=deque([-1,-1],maxlen=2)
prev_val=0
match=False
toss_time=False
def nod(x):
    if x<0:
        return -1 * x
    else:
        return x
toss=True
bat=False
bowl=False
target=0
chase=0
result=False
t=0
T=0
toss_result=False
def same(array):
    for i in range (1,len(array)):
        if array[0] != array[i]:
            return False
    return True
while True:
    index_y=0
    index_x=0
    finger=[0]*5
    boo,img=cap.read()
    img=cv2.flip(img,1)
    h,w,d=img.shape
    img_rec=cv2.rectangle(img,(90,420),(135,450),(225,0,0),-1)
    img_rect=img_rec.copy()

    img_rgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    res=my_hand.process(img_rgb)
    if res.multi_hand_landmarks:
        for one_hand in res.multi_hand_landmarks:
            wr_x=one_hand.landmark[0].x
            fr_x=one_hand.landmark[17].x
            wr_y=one_hand.landmark[0].y
            fr_y=one_hand.landmark[17].y
            index_x=one_hand.landmark[8].x
            index_y=one_hand.landmark[8].y

            index_tip_x=(one_hand.landmark[8].x)-wr_x
            middle_tip_x=(one_hand.landmark[12].x)-wr_x
            index_pip_x=(one_hand.landmark[6].x)-wr_x
            middle_pip_x=(one_hand.landmark[10].x)-wr_x
            middle_pip_y=(one_hand.landmark[10].y)-wr_y
            ring_tip_x=(one_hand.landmark[16].x)-wr_x
            ring_tip_y=(one_hand.landmark[16].y)-wr_y
            ring_pip_y=(one_hand.landmark[14].y)-wr_y
            ring_pip_x=(one_hand.landmark[14].x)-wr_x
            pinky_tip_x=(one_hand.landmark[20].x)-wr_x
            pinky_tip_y=(one_hand.landmark[20].y)-wr_y
            pinky_pip_y=(one_hand.landmark[18].y)-wr_y
            pinky_pip_x=(one_hand.landmark[18].x)-wr_x
            thumb_pip_x=(one_hand.landmark[3].x)-fr_x
            thumb_pip_y=(one_hand.landmark[3].y)-fr_y
            thumb_tip_y=(one_hand.landmark[4].y)-fr_y
            thumb_tip_x=(one_hand.landmark[4].x)-fr_x

            index_tip_y=(one_hand.landmark[8].y)-wr_y
            middle_tip_y=(one_hand.landmark[12].y)-wr_y
            index_pip_y=(one_hand.landmark[6].y)-wr_y
            dist8=index_tip_x**2+index_tip_y**2
            dist6=index_pip_x**2+index_pip_y**2
            dist3=thumb_pip_x**2+thumb_pip_y**2
            dist4=thumb_tip_x**2+thumb_tip_y**2
            dist12 = middle_tip_x ** 2 + middle_tip_y ** 2
            dist10 = middle_pip_x**2+middle_pip_y**2
            dist16=ring_tip_x**2+ring_tip_y**2
            dist20=pinky_tip_x**2+pinky_tip_y**2
            dist18=pinky_pip_x**2+pinky_pip_y**2
            dist14=ring_pip_x**2+ring_pip_y**2
            if dist3>dist4:
                finger[0]=1
            if dist6>=dist8:

                finger[1]=1
            if dist10>=dist12:
                finger[2]=1
            if dist14>=dist16:

                finger[3]=1
            if dist18>=dist20:

                finger[4]=1
            no=0
            if finger==[1,0,1,1,1]:
                choose=True
            else:
                choose=False
            if finger == [0, 1, 1, 1, 1]:
                no = 6
            else:
                for fing in finger:

                    if fing == 0:
                        no += 1
            if no==0:
                closed=True
            else:
                closed=False
            prev_no.append(no)
            if same(prev_no):
                val=prev_no[0]
                if prev_val == 0:
                    prev_val=val
                    cv2.putText(img_rec, str(val), (100, 440), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
                    print(prev_val)
                elif val == 0:
                    prev_val=0
                    cv2.putText(img_rec,"---", (100, 440), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
            mpdraw.draw_landmarks(img, one_hand, hand.HAND_CONNECTIONS)

    if not match:

        if choose and 210<nod(index_x*w)<390:
            if 220<nod(index_y*h)<260:
                match=True
                cv2.rectangle(img_rec, (200, 210), (400, 270), (0, 255, 0))
                cv2.putText(img_rec, "New game", (290, 240), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0))
                wait=True
            else:
                cv2.rectangle(img_rec, (200, 210), (400, 270), (0, 0, 255))
                cv2.putText(img_rec, "New game", (250, 240), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 225))
        else:
            cv2.rectangle(img_rec, (200, 210), (400, 270), (0, 0, 255))
            cv2.putText(img_rec, "New game", (250, 240), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 225))

    if match:
        T=T+1
        if T != 1 and toss:

            if choose and 160<index_x * 640 <290 and 220<index_y * 480<260:
                coin=1
                cv2.rectangle(img_rec, (150, 210), (300, 270), (0, 255, 0))
                cv2.putText(img_rec, "odd", (160, 240), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0))
                cv2.rectangle(img_rec, (400, 210), (550, 270), (0, 0, 255))
                cv2.putText(img_rec, "even", (450, 240), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 225))
                toss=False
                toss_time=True
                wait=True
                print("odd")

            elif choose and 410<index_x * 640 <540 and 220<index_y * 480<260:
                coin=0
                cv2.rectangle(img_rec, (150, 210), (300, 270), (0, 0, 255))
                cv2.putText(img_rec, "odd", (160, 240), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 225))
                cv2.rectangle(img_rec, (400, 210), (550, 270), (0, 255, 0))
                cv2.putText(img_rec, "even", (450, 240), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0))
                toss = False
                toss_time = True
                print("even")
                wait=True

            else:
                cv2.rectangle(img_rec, (150, 210), (300, 270), (0, 0, 255))
                cv2.putText(img_rec, "odd", (160, 240), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 225))
                cv2.rectangle(img_rec, (400, 210), (550, 270), (0, 0, 255))
                cv2.putText(img_rec, "even", (450, 240), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 225))
                toss_time = False
                print(index_x,index_y)
        elif toss_time:
            if res.multi_hand_landmarks:

                if t<90:
                    if t !=0:
                        cv2.putText(img_rec, "close and open ur hand", (100, 250), cv2.FONT_HERSHEY_TRIPLEX, 1,
                                    (255, 0, 0))

                    t=t+1
                else:
                    close_open.append(prev_val)
                    if close_open[0]==0:
                        if close_open[1]!=0:
                            head=close_open[1]
                            tail=randint(0,6)
                            cv2.rectangle(img_rec, (150, 210), (300, 270), (0, 0, 255))
                            cv2.putText(img_rec, str(head), (160, 240), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 225))
                            cv2.putText(img_rec, str(tail), (450, 240), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 225))
                            cv2.putText(img_rec, "You", (160, 190), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 225))
                            cv2.rectangle(img_rec, (400, 210), (550, 270), (0, 0, 255))
                            cv2.putText(img_rec, "computer", (450, 190), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 225))
                            toss_time = False
                            wait=True
                            toss_result=True

                            if (head + tail)%2==coin:
                                cv2.putText(img_rec, "you Won", (300, 100), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0))

                                toss_won=True
                            else:
                                cv2.putText(img_rec, "computer won", (300, 190), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 225))
                                toss_won=False
        elif toss_result:
            if toss_won == True:
                s = s + 1
                if s != 1:

                    if choose and 160< index_x *640 <290 and 220< index_y * 480<260:
                        cv2.rectangle(img_rec, (150, 210), (300, 270), (0, 255, 0))
                        cv2.putText(img_rec, "bat", (160, 240), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 225))
                        cv2.rectangle(img_rec, (400, 210), (550, 270), (0, 0, 255))
                        cv2.putText(img_rec, "bowl", (450, 240), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 225))

                        bat=True
                        first_innings=True
                        second_innings=False
                        wait=True
                        toss_result=False
                    elif choose and 410< index_x * 640 <540 and 220< index_y *480<260:
                        cv2.rectangle(img_rec, (150, 210), (300, 270), (0, 0, 255))
                        cv2.putText(img_rec, "bat", (160, 240), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 225))
                        cv2.rectangle(img_rec, (400, 210), (550, 270), (0, 255, 0))
                        cv2.putText(img_rec, "bowl", (450, 240), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 225))

                        bowl=True
                        first_innings=True
                        wait=True
                        toss_result=False
                    else:
                        cv2.rectangle(img_rec, (150, 210), (300, 270), (0, 0, 255))
                        cv2.putText(img_rec, "bat", (160, 240), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 225))
                        cv2.rectangle(img_rec, (400, 210), (550, 270), (0, 0, 255))
                        cv2.putText(img_rec, "bowl", (450, 240), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 225))
            elif not toss_won:
                print("computer won toss")
                bat_bowl=randint(0,1)
                if bat_bowl==0:
                    bat=True
                    first_innings=True
                else:
                    bowl=True
                    first_innings=True
                toss_result=False
        if bat or bowl:
            if bowl:
                ball = randint(1, 6)
                cv2.rectangle(img_rec, (100, 5), (300, 55), (0, 255, 255), -1)
                cv2.rectangle(img_rec, (400, 5), (600, 55), (255, 0, 0), -1)
                cv2.putText(img_rec, "computer", (150, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))
                cv2.putText(img_rec, "you", (402, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))
                cv2.rectangle(img_rec, (150, 210), (300, 270), (0, 0, 255))
                cv2.putText(img_rec, str(prev_val), (160, 240), cv2.FONT_HERSHEY_TRIPLEX, 1,
                            (0, 0, 225))
                cv2.putText(img_rec, str(target), (160, 55), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 225))
                cv2.putText(img_rec, str(chase), (450, 55), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 225))
                cv2.putText(img_rec, "You", (160, 190), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 225))
                cv2.rectangle(img_rec, (400, 210), (550, 270), (0, 0, 255))
                cv2.putText(img_rec, "computer", (450, 190), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 225))
                close_open.append(prev_val)
                if first_innings:
                    print("first innings")
                    if close_open[0] == 0 and prev_val != 0 and prev_val != ball:
                        cv2.putText(img_rec, str(ball), (450, 240), cv2.FONT_HERSHEY_TRIPLEX, 1,
                                    (0, 0, 225))

                        target = target + ball
                        wait=True
                    elif close_open[0] == 0 and prev_val == ball:
                        cv2.putText(img_rec, str(ball), (450, 240), cv2.FONT_HERSHEY_TRIPLEX, 1,
                                    (0, 0, 225))
                        cv2.putText(img_rec, "computer have scored" + str(target) + "runs", (100, 460),
                                    cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 225))
                        wait = True

                        first_innings = False
                else:
                    if chase <= target:
                        if close_open[0] == 0 and prev_val != 0 and prev_val != ball:
                            cv2.putText(img_rec, str(ball), (450, 240), cv2.FONT_HERSHEY_TRIPLEX, 1,
                                        (0, 0, 225))

                            chase = chase + prev_val
                        elif close_open[0] == 0 and prev_val == ball:
                            ball=False
                            if chase <= target:
                                result=True
                                bat=False
                                ball=False
                                img_rec=img_rect

                                if chase < target:

                                    cv2.putText(img_rec,
                                                "computer won by" + str(target - chase) + "runs",
                                                (200, 300),
                                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
                                else:
                                    cv2.putText(img_rec, "match draw", (200, 300),
                                                cv2.FONT_HERSHEY_SIMPLEX, 1,
                                                (0, 255, 0))

                                cv2.putText(img_rec, "play again", (200, 50), cv2.FONT_HERSHEY_SIMPLEX,
                                            1,
                                            (0, 0, 255))
                                cv2.rectangle(img_rec, (200,25), (350, 100), (0, 255, 0))
                                if choose and 210 < index_x * 640 < 340 and 25 < index_y * 480 < 90:
                                    t = 0
                                    wait = False

                                    closed = True
                                    prev_no = deque([0, 0, 0, 0, 0], maxlen=10)
                                    close_open = deque([-1, -1], maxlen=2)
                                    prev_val = 0
                                    match = False
                                    toss_time = False
                                    toss = True
                                    bat = False
                                    bowl = False
                                    target = 0
                                    chase = 0
                                    t = 0
                                    T = 0
                                    toss_result = False
                    else:
                        ball=False
                        bat=False
                        result=True
                        img_rec=img_rect

                        cv2.putText(img_rec, "You won the match", (300, 300), cv2.FONT_HERSHEY_SIMPLEX,
                                    1,
                                    (0, 255, 0))

                        cv2.putText(img_rec, "play again", (250, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (0, 0, 255))
                        cv2.rectangle(img_rec, (200, 25), (350, 100), (0, 255, 0))
                        if choose and 210 < index_x * 640 < 350 and 25 < index_y * 480 < 90:
                            t = 0
                            wait = False
                            closed = True
                            prev_no = deque([0, 0, 0, 0, 0], maxlen=10)
                            close_open = deque([-1, -1], maxlen=2)
                            prev_val = 0
                            match = False
                            toss_time = False
                            toss = True
                            bat = False
                            bowl = False
                            target = 0
                            chase = 0
                            t = 0
                            T = 0
                            toss_result = False



            if bat:
                ball=randint(1,6)
                cv2.rectangle(img_rec,(100,5),(300,55),(0,255,255),-1)
                cv2.rectangle(img_rec,(400,5),(600,55),(255,0,0),-1)
                cv2.putText(img_rec,"you",(150,25),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0))
                cv2.putText(img_rec,"computor",(402,25),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0))
                cv2.rectangle(img_rec, (150, 210), (300, 270), (0, 0, 255))
                cv2.putText(img_rec, str(prev_val), (160, 240), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 225))
                cv2.putText(img_rec, str(target), (160, 55), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 225))
                cv2.putText(img_rec, str(chase), (450, 55), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 225))
                cv2.putText(img_rec, "You", (160, 190), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 225))
                cv2.rectangle(img_rec, (400, 210), (550, 270), (0, 0, 255))
                cv2.putText(img_rec, "computer", (450, 190), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 225))
                close_open.append(prev_val)
                if first_innings:
                    if close_open[0]==0 and prev_val !=0 and prev_val != ball:
                        cv2.putText(img_rec, str(ball), (450, 240), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 225))

                        target = target + prev_val
                        wait=True
                    elif close_open[0]==0 and prev_val == ball:
                        cv2.putText(img_rec, str(ball), (450, 240), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 225))
                        cv2.putText(img_rec, "you have scored"+str(target)+"runs", (100, 460), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 225))
                        wait=True


                        first_innings=False
                else:
                    if chase<=target:
                        if close_open[0]==0 and prev_val != 0 and prev_val != ball:
                            cv2.putText(img_rec, str(ball), (450, 240), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 225))

                            chase = chase + ball
                            wait=True
                        elif close_open[0]==0 and prev_val == ball:
                            print("you lost")
                            if chase<=target:
                                result=True
                                bat=False
                                ball=False
                                img_rec=img_rect

                                if chase<target:

                                    cv2.putText(img_rec, "you won by" + str(target - chase) + "runs", (100, 460),
                                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
                                else:
                                    cv2.putText(img_rec, "match draw", (100, 460), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                                (0, 255, 0))

                                cv2.putText(img_rec,"play again",(240,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255))
                                cv2.rectangle(img_rec,(200,25),(350,100),(0,255,0),-1)
                                if choose and 210<index_x*640<340 and 25 <index_y*480<90:
                                    t = 0
                                    wait = False

                                    closed = True
                                    prev_no = deque([0, 0, 0, 0, 0], maxlen=10)
                                    close_open = deque([-1, -1], maxlen=2)
                                    prev_val = 0
                                    match = False
                                    toss_time = False
                                    toss = True
                                    bat = False
                                    bowl = False
                                    target = 0
                                    chase = 0
                                    t = 0
                                    T = 0
                                    toss_result = False
                    else:
                        bat=False
                        ball=False
                        result=True
                        img_rec=img_rect

                        cv2.putText(img_rec, "match lost", (100, 360), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (0, 255, 0))

                        cv2.putText(img_rec, "play again", (200, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
                        cv2.rectangle(img_rec, (200, 25), (350, 100), (0, 255, 0), -1)
                        if choose and 210 < index_x * 640 < 350 and 25 < index_y * 480 < 90:
                            t = 0
                            wait = False

                            closed = True
                            prev_no = deque([0, 0, 0, 0, 0], maxlen=10)
                            close_open = deque([-1, -1], maxlen=2)
                            prev_val = 0
                            match = False
                            toss_time = False
                            toss = True
                            bat = False
                            bowl = False
                            target = 0
                            chase = 0
                            t = 0
                            T = 0
                            toss_result = False
        if result:
            print("result")
            cv2.putText(img_rec, "play again", (200, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255))
            cv2.rectangle(img_rec, (200, 25), (350, 100), (0, 255, 0))
            if choose and 210 < index_x * 640 < 340 and 25 < index_y * 480 < 90:
                t = 0
                wait = False

                closed = True
                prev_no = deque([0, 0, 0, 0, 0], maxlen=10)
                close_open = deque([-1, -1], maxlen=2)
                prev_val = 0
                match = False
                toss_time = False
                toss = True
                bat = False
                bowl = False
                target = 0
                chase = 0
                t = 0
                T = 0
                toss_result = False
                result=False







    cv2.imshow('hand cricket',img_rec)
    if cv2.waitKey(2) & 0xFF==ord('q'):
        break
    if cv2.waitKey(1) & 0xFF == ord("m"):
        match = True
    if wait:
        time.sleep(1)
    wait=False
    choose=False




