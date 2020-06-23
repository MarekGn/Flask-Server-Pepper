#!/usr/bin/python
# -*- coding: utf8 -*-

from flask import Flask, request, jsonify
import qi
global session
global posture_service
global motion_service
global tabletService
global textService

app = Flask(__name__)

NAO_IP = '192.168.1.123'
NAO_PORT = '9559'

SERVER_IP = "192.168.1.102"
SERVER_PORT = "5000"

@app.route('/')
def start():
    global session, posture_service, motion_service, tabletService, textService
    session = qi.Session()
    session.connect("tcp://{}:{}".format(NAO_IP, NAO_PORT))
    posture_service = session.service("ALRobotPosture")
    motion_service = session.service("ALMotion")
    tabletService = session.service("ALTabletService")
    textService = session.service("ALTextToSpeech")
    return "Connection with robot established"


@app.route('/speech', methods=['POST'])
def speech():
    # Pepper API calls go here
    content = request.json
    text = content["speech_text"]
    print("saying: {}".format(text))
    textService.setVoice("naoenu")
    textService.setLanguage("Polish")
    textService.setVolume(0.8)
    textService.setParameter("speed", 100)
    textService.say(text)
    print("end")
    return "Success", 200


@app.route('/move', methods=['POST'])
def move_forward():
    # # Pepper API calls go here
    content = request.json
    mov_type = content["movement_type"]
    distance = content["distance"]
    angle = content["angle"]
    posture_service.goToPosture("Stand", 0.5)
    if mov_type == "FORWARD":
        motion_service.moveTo(float(distance), 0, 0, 5)
    elif mov_type == "BACKWARD":
        motion_service.moveTo(float(-distance), 0, 0, 5)
    elif mov_type == "LEFT":
        motion_service.moveTo(0, 0, float(angle), 5)
    elif mov_type == "RIGHT":
        motion_service.moveTo(0, 0, float(-angle), 5)
    return "Success", 200


if __name__ == '__main__':
    app.run()
