import sys
from Adafruit_IO import MQTTClient
import time
import random
from simple_ai import *
from uart import readSerial, writeData

AIO_FEED_IDs = ["nutnhan1", "nutnhan2", "ai"]
AIO_USERNAME = "michaelnguyen"
AIO_KEY = "aio_bfvL47pz2qU938Nospw9eWYpiJKl"

def connected(client):
    print("Ket noi thanh cong ...")
    for topic in AIO_FEED_IDs:
        client.subscribe(topic)
    #client.subscribe(AIO_FEED_ID)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit(1)

def message(client , feed_id , payload):    
    print("Nhan du lieu: " + payload + " feed id: " + feed_id)
    if (feed_id == "nutnhan1"):
        if payload == "0":
            writeData("1")
            print("Write data 1")
        else:
            writeData("2")
            print("Write data 2")
    if (feed_id == "nutnhan2"):
        if payload == "0":
            writeData("3")
            print("Write data 3")
        else:
            writeData("4")
            print("Write data 4")
    if (feed_id == "ai"):
        if payload == "None\n":
            writeData("5")
            print("Write data 5")
        elif (payload == "Mask\n"):
            writeData("6")
            print("Write data 6")
        else:
            writeData("7")
            print("Write data 7")


client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()
counter = 10
sensor_type = 0
counter_ai = 5
ai_result = ""
previous_ai_result = ""

def randomDataPublish(counter, sensor_type):
    counter = counter - 1
    if counter <= 0:
        counter = 10
        print("Random data is publishing...")
        if sensor_type == 0:
            print("Temperature...")
            temp = random.randint(10, 20)
            client. publish("cambien1", 26.6)
            sensor_type = 1
        elif sensor_type == 1:
            print("Humidity...")
            humi = random.randint(50, 70)
            client.publish("cambien2", humi)
            sensor_type = 2
        elif sensor_type == 2:
            print("Light...")
            light = random.randint(100, 500)
            client.publish("cambien3", 51.1)
            sensor_type = 0
    return counter, sensor_type

def maskRecognition(counter_ai, ai_result, previous_ai_result):
    counter_ai = counter_ai - 1
    if counter_ai <= 0:
        counter_ai = 5
        className, confidenceScore = image_detector()
        print(ai_result)
        #ai_result = f"{className}: {confidenceScore}%"
        ai_result = f"{className}"
        # if (previous_ai_result != ai_result):            
        #     client.publish("ai", ai_result)
        # previous_ai_result = ai_result
        client.publish("ai", ai_result)
    return counter_ai, ai_result, previous_ai_result

#background loop
while True:
    #Ramdom data publishing
    #counter, sensor_type = randomDataPublish(counter, sensor_type)

    #simple ai publishing
    counter_ai, ai_result, previous_ai_result = maskRecognition(counter_ai, ai_result, previous_ai_result)

    #uart
    readSerial(client)


    time.sleep(1)

    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break
camera.release()
cv2.destroyAllWindows()