from flask import Flask, render_template, request
import time
import RPi.GPIO as GPIO
from adafruit_htu21d import HTU21D
import busio
app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

sda = 2 # GPIO 핀 번호, sda라고 이름이 보이는 핀
scl = 3 # GPIO 핀 번호, scl이라고 이름이 보이는 핀
i2c = busio.I2C(scl, sda)
sensor = HTU21D(i2c) # HTU21D 장치를 제어하는 객체 리턴

@app.route('/')
def index():
        return render_template('mqttHtml.html')

@app.route('/checktemp/', methods=['GET'])
def temp():
        hum = int(sensor.relative_humidity)
        temper = int(sensor.temperature)
        return render_template('temper.html', hum = hum, temper = temper)

if __name__ == "__main__":
        app.run(host='0.0.0.0', port=8080)