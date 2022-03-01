from flask import Flask
from dataclasses import dataclass
from flask import request
from typing import Any
from flask import json
from datetime import datetime
app = Flask(__name__)


@dataclass
class Project(object):
    projectID: str
    name: str
    numberOfDevice: int
    remark: str = ""


@dataclass
class Device(object):
    deviceID: str
    inProjectID: str
    numberOfSensors: int
    sensors: list


@dataclass
class Sensor(object):
    sensorType: str
    inDeviceID: str


@dataclass
class SensorRecord(object):
    sensorType: str
    inDeviceID: str
    measurement: Any
    timeStramp: str


def makeRespose(res, code: int = 0, msg: str = "ok"):
    json_r = json.dumps(
        {"code": code, "msg": msg, "data": res},
        ensure_ascii=False,
    )
    print(json_r)
    return app.response_class(
        response=json_r,
        mimetype="application/json",
    )


projects = [Project("p001", "仓库书画监测", 2, "测试数据project1"), Project("p002", "2月27日运输监测监测", 1)]
devices = [Device("device011", "p001", 2, [Sensor("Temperature", "device011"), Sensor("Humidity", "device011")])]
sensor_records = [SensorRecord("Temperature", "device011", 25.0, datetime.now().timestamp()), SensorRecord("Humidity", "device011", 43, datetime.now().timestamp())]


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/project", methods=["GET", "POST"])
def project():
    if request.method == "GET":
        projectID = request.args.get('id', None)
        if projectID is None:
            # 全部
            res = projects
        else:
            res = [projects[0]]
        return makeRespose(res)
    elif request.method == "POST":
        # 处理创建
        return makeRespose("")


@app.route("/device", methods=["GET", "POST", "PUT"])
def device():
    if request.method == "GET":
        deviceID = request.args.get('id', None)
        if deviceID is None:
            # 全部
            res = devices
        else:
            res = [devices[0]]
        return makeRespose(res)


@app.route("/sensor-record")
def sensorRecord():
    return makeRespose(sensor_records)
