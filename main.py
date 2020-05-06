import cv2
from flask import Flask,render_template,request,flash,redirect,url_for
from utils import *
import numpy as np
from matplotlib import pyplot as plt
from playsound import playsound
import os
import json
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "images//"
app.config["CACHE_TYPE"] = "null"
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'



@app.route('/',methods=['GET','POST'])
def home():
    address = "static/result/res" + str(1) + ".jpg"
    print(address)
    return render_template('index.html',addr=address)

@app.route('/detect',methods=['GET','POST'])
def detect():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], "test.jpg"))

    notes=["10.jpg","10_new.jpg","20.jpg","20_new.jpg","50.jpg","50_new.jpg","100.jpg","100_new.jpg","200.jpg","500.jpg","2000.jpg","test.jpg"]
    res = []

    for i in range(len(notes)-1):
        img1 = cv2.imread("images//"+notes[i],0)
        img2 = cv2.imread("images//"+notes[11], 0)
        img1 = resize_img(img1, 0.5)
        img2 = resize_img(img2, 0.2)
        # ORB Detector
        orb = cv2.ORB_create()
        kp1, des1 = orb.detectAndCompute(img1, None)
        kp2, des2 = orb.detectAndCompute(img2, None)
        #print(des1)
        # Brute Force Matching
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)
        #print(matches)
        print(len(matches))
        res.append(len(matches))
        matches = sorted(matches, key = lambda x:x.distance)
        matching_result = cv2.drawMatches(img1, kp1, img2, kp2, matches[:50], None, flags=2)




        #cv2.imshow("Test", img2)

        start_point = (0, 0)
        end_point = (0,0)
        color = (0, 0, 0)
        thickness = 0
        image = cv2.rectangle(img2, start_point, end_point, color, thickness)
        #cv2.imshow("result", image)

        #cv2.imshow("Matching result", matching_result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    val = res.index(max(res))
    print(res.index(max(res)))
    font = cv2.FONT_HERSHEY_SIMPLEX
    deno = 0
    if (val == 0 or val == 1):
        deno = 10
    elif (val == 2 or val == 3):
        deno = 20
    elif (val == 4 or val == 5):
        deno = 50
    elif (val == 6 or val == 7):
        deno = 100
    elif (val == 8):
        deno = 200
    elif (val == 9):
        deno = 500
    else:
        deno = 2000

    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (25, 25)
    fontScale = 1
    color = (255, 0, 0)
    thickness = 2
    image = cv2.putText(image, 'Currency Amount Detected is ' + str(deno) + ' INR', org, font,
                        fontScale, color, thickness, cv2.LINE_AA)
    flash('Currency Amount Detected is ' + str(deno) + ' INR')
    with open('config.json') as f:
        data = json.load(f)
    cnt=data['params']['count']
    data['params']['count']=data['params']['count']+1
    with open('config.json', 'w') as f:
        json.dump(data, f)
    name="res"+str(cnt)+".jpg"
    cv2.imwrite("static//result//"+name,image)
    address="static/result/res"+str(cnt)+".jpg"
    print(address)
    return render_template('index.html', addr=address)

if __name__=="__main__":
     app.run(port=5000, debug=True)