import cv2
from flask import Flask,render_template,request,flash,redirect,url_for
from utils import *
import numpy as np
from matplotlib import pyplot as plt
from playsound import playsound
import subprocess
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "images//"
app.config["CACHE_TYPE"] = "null"
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'



