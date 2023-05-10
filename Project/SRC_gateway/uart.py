#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import serial.tools.list_ports
import random
import time
import  sys
from  Adafruit_IO import  MQTTClient

AIO_FEED_IDs = [""]
AIO_USERNAME = ""
AIO_KEY = ""
# AIO_FEED_IDs = ["cambien1", "cambien2"]
# AIO_USERNAME = "michaelnguyen"
# AIO_KEY = "aio_bfvL47pz2qU938Nospw9eWYpiJKl"

# def  connected(client):
#     print("Ket noi thanh cong...")
# #     client.subscribe(AIO_FEED_ID)
#     for topic in AIO_FEED_IDs:
#         client.subscribe(topic)

# def  subscribe(client , userdata , mid , granted_qos):
#     print("Subcribe thanh cong...")

# def  disconnected(client):
#     print("Ngat ket noi...")
#     sys.exit (1)

# def  message(client , feed_id , payload):
#     print("Nhan du lieu: " + payload)
#     ser.write((str(payload) + "#").encode())

# client = MQTTClient(AIO_USERNAME , AIO_KEY)
# client.on_connect = connected
# client.on_disconnect = disconnected
# client.on_message = message
# client.on_subscribe = subscribe
# client.connect()
# client.loop_background()

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB Serial Device" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    #return commPort
    return "COM3"

ser = serial.Serial( port=getPort(), baudrate=115200)

mess = ""
def processData(client, data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    if splitData[1] == "T":
        client.publish("cambien1", splitData[2])
    elif splitData[1] == "H":
        client.publish("cambien2", splitData[2])

mess = ""
def readSerial(client):
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(client, mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]

def writeData(data):
    ser.write(str(data).encode());

# while True:
#     readSerial(client)
#     time.sleep(1)

