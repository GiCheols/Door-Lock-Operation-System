import os
import io
import cv2
import time
from adafruit_htu21d import HTU21D
import busio
import RPi.GPIO as GPIO
from PIL import Image, ImageFilter

trig = 20
echo = 16
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)
GPIO.output(trig, False)

sda = 2
scl = 3
i2c = busio.I2C(scl, sda)
sensor = HTU21D(i2c)
led = 5
ledPass = 6

GPIO.setup(led, GPIO.OUT)
GPIO.setup(ledPass, GPIO.OUT)

fileName = ""

def takePicture():
    global fileName
    global camera

    camera = cv2.VideoCapture(0, cv2.CAP_V4L)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if len(fileName) != 0:
        os.unlink(fileName)
    

    ret, frame = camera.read()
    
    takeTime = time.time()
    fileName = "./static/%d.jpg" % (takeTime * 10)
    cv2.imwrite(fileName, frame)
    camera.release()
    return fileName


def measureDistance():
    global trig, echo
    time.sleep(3.0) # 3초마다 거리를 재도록 설정
    GPIO.output(trig, True) # 신호 1
    GPIO.output(trig, False) # 신호가 1-> 0으로 떨어질 때 초음파발생
    
    while(GPIO.input(echo) == 0):
        pass

    pulse_start = time.time() # echo 신호가 1인 경우, 초음파 발사된 순간

    while(GPIO.input(echo) == 1):
        pass

    pulse_end = time.time() # 초음파 신호가 도착한 순간
# echo 신호가 1->0으로 되면 보낸 초음파 수신 완료
    
    pulse_duration = pulse_end - pulse_start
    distance = 340*100/2*pulse_duration
    return 340*100/2*pulse_duration

def onLed(onOff):
    GPIO.output(led, onOff)
