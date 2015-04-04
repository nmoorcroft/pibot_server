#!/usr/bin/env python
import json
import time
import RPi.GPIO as GPIO
from flask import Flask
from flask import Response
from flask import request

app = Flask(__name__)
ins = []

@app.route('/api/go', methods=['GET'])
def go():
    for i in ins:
        cmd = i.items()[0]
        if cmd[0] == 'forward':
            forward(cmd[1])
        if cmd[0] == 'right':
            right(cmd[1])
        if cmd[0] == 'left':
            left(cmd[1])

    resp = json.dumps(ins)
    return Response(resp, mimetype='application/json')


@app.route('/api/left', methods=['GET'])
def addleft():
    count = request.args.get('dist')
    ins.append({'left': int(count)})
    return Response(json.dumps(ins), mimetype='application/json')

@app.route('/api/right', methods=['GET'])
def addright():
    count = request.args.get('dist')
    ins.append({'right': int(count)})
    return Response(json.dumps(ins), mimetype='application/json')


@app.route('/api/forward', methods=['GET'])
def addforward():
    count = request.args.get('dist')
    ins.append({'forward': int(count)})
    return Response(json.dumps(ins), mimetype='application/json')


@app.route('/api/list', methods=['GET'])
def list():
    return Response(json.dumps(ins), mimetype='application/json')

@app.route('/api/clear', methods=['GET'])
def clear():
    del ins[:]
    return Response(json.dumps(ins), mimetype='application/json')


@app.route('/api/del', methods=['GET'])
def pop():
    ins.pop()
    return Response(json.dumps(ins), mimetype='application/json')


def right(count):
    GPIO.output(4, GPIO.HIGH)
    GPIO.output(7, GPIO.LOW)
    time.sleep(count / 10)
    GPIO.output(4, GPIO.LOW)
    GPIO.output(7, GPIO.LOW)


def left(count):
    GPIO.output(4, GPIO.LOW)
    GPIO.output(7, GPIO.HIGH)
    time.sleep(count / 10)
    GPIO.output(4, GPIO.LOW)
    GPIO.output(7, GPIO.LOW)


def forward(count):
    GPIO.output(4, GPIO.HIGH)
    GPIO.output(7, GPIO.HIGH)
    time.sleep(count / 10)
    GPIO.output(4, GPIO.LOW)
    GPIO.output(7, GPIO.LOW)


if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.cleanup()
    GPIO.setup(4, GPIO.OUT)
    GPIO.setup(7, GPIO.OUT)
    app.run(host='0.0.0.0')




