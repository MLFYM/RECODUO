from django.conf import settings
import numpy as np
import cv2
import warnings
import os
import copy
from sklearn.externals import joblib
import numpy as np
from keras.models import load_model
import matplotlib.pyplot as plt
from django.conf import settings
import time
from .apps import Lmodel, Lgraph, sess
from tensorflow.python.keras.backend import set_session

def deep_face(path):

    image_size = (250, 250)
    start = time.time()

    src = cv2.imread(path)
    src = cv2.flip(src, 1)

    s2 = time.time()-start
    print(" imread 걸린시간 : {} ".format(s2))
    start = time.time()

    # modelh5= settings.MODEL_ROOT + '/MobileNetV2(full).h5'        #모바일넷 12초 덴스넷 54초 모바일넷2 12초
    # model = load_model(modelh5)
    model = Lmodel

    s3 = time.time()-start
    print(" model load 걸린시간 : {} ".format(s3))
    start = time.time()

    cascade_file = settings.MODEL_ROOT + '/haarcascade_frontface.xml'
    cascade = cv2.CascadeClassifier(cascade_file)

    s4 = time.time()-start
    print(" 캐스캐이드 load 걸린시간 : {}".format(s4))
    start = time.time()

    # 이전 프레임과 비교를 위해 흑백으로 변환하기 --- (*2)
    # gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    face_list = cascade.detectMultiScale(src)

    # if face_list == None:


    for (x,y,w,h) in face_list:
        roi = src[y:y+h, x:x+w]
        roi = roi.astype('float32')/255
        imagex = cv2.resize(roi, image_size)
        print(imagex.shape)

        s5 = time.time()-start
        print(" resize 걸린시간 : {}".format(s5))
        start = time.time()

#         plt.imshow(cv2.cvtColor(imagex, cv2.COLOR_BGR2RGB))
#         plt.show()
        image_data = imagex.reshape(1, 250, 250, 3)

        s6 = time.time()-start
        print(" reshape 걸린시간 : {}".format(s6))
        start = time.time()

        color_0 = (0, 234, 23) #(0,198,255) #(95, 4, 180)
        color_1 = (249, 0, 4)
        color_2 = (27, 14, 224)



        print("**정상1**")

        with Lgraph.as_default():
            set_session(sess)
            pred_y = model.predict(image_data) # --- (*4)

        print("**정상2**")

        print(pred_y)

        print("**정상3**")

        # if np.max(pred_y) == pred_y[0][0]:
        #     val = 0
        # elif np.max(pred_y) == pred_y[0][1]:
        #     val = 1
        # else:
        #     val = 2

        if np.argmax(pred_y) == 0:
            val = 0
        elif np.argmax(pred_y) == 1:
            val = 1
        else:
            val = 2


        s7 = time.time()-start
        print(" predict 걸린시간 : {}".format(s7))
        start = time.time()
        print(np.argmax(pred_y))

        if np.argmax(pred_y) == 0:
                cv2.rectangle(src, (x, y), (x+w, y+h), color_0, thickness=2)
                cv2.putText(src,'Neutral',(x,y-10),cv2.FONT_ITALIC, 1.2, (255,255,255), thickness=2)

        elif np.argmax(pred_y) == 1:
                cv2.rectangle(src, (x, y), (x+w, y+h), color_1, thickness=2)
                cv2.putText(src,'Positive',(x,y-10),cv2.FONT_ITALIC, 1.2, (255,255,255), thickness=2)

        else:
            # np.argmax(pred_y) == 2:
            cv2.rectangle(src, (x, y), (x+w, y+h), color_2, thickness=2)
            cv2.putText(src,'Negative',(x,y-10),cv2.FONT_ITALIC, 1.2, (255,255,255), thickness=2)

        cv2.imwrite(path + '2.jpeg', src)

        return val, pred_y
        # val

    cv2.imwrite(path + '2.jpeg', src)
    return 3

            # cv2.imshow('src', src)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
