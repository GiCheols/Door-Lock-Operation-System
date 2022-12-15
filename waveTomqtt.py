import time
import paho.mqtt.client as mqtt
import circuitGiCheol


broker_ip = "localhost"

def on_connect(client, userdata, flag, rc):
    client.subscrive("facerecognition", qos = 0)

def on_message(client, userdata, msg):
    global flag
    command = msg.payload.decode("utf-8")
    if command == "action":
        print("사진 촬영을 시작합니다")
        flag = True

client = mqtt.Client()
client.connect(broker_ip, 1883)
client.loop_start()

while(True):
    distance = circuitGiCheol.measureDistance()
    if(distance <= 30.0):
        circuitGiCheol.onLed(1)
        imageFileName = circuitGiCheol.takePicture()
        print(imageFileName)
        client.publish("image", imageFileName, qos = 0)
        flag = False
        
    else:
        circuitGiCheol.onLed(0)
    client.publish("ultrasonic", distance, qos = 0)

client.loop_stop()
client.disconnect()