from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass

db = SQLAlchemy()


@dataclass
class Project(db.Model):
    projectID: str = db.Column(db.String, primary_key=True)
    name: str = db.Column(db.String, nullable=False)
    remark: str = db.Column(db.Text, nullable=False)
    devices = db.relationship("Device", backref="Project", lazy=True)


@dataclass
class Sensor(db.Model):
    sensorType: str = db.Column(db.String, primary_key=True)
    deviceID: str = db.Column(db.String, db.ForeignKey("device.deviceID"), primary_key=True)


@dataclass
class Device(db.Model):
    deviceID: str = db.Column(db.String, primary_key=True)
    projectID: str = db.Column(db.String, db.ForeignKey(Project.projectID), nullable=False)
    sensors = db.relationship("Sensor", backref="Device", lazy=True)
    numberOfSensors: int = db.column_property(db.select([db.func.count(Sensor.sensorType)]).where(Sensor.deviceID == deviceID))


@dataclass
class SensorRecord(db.Model):
    sensorType: str = db.Column(db.String, db.ForeignKey(Sensor.sensorType), nullable=False, primary_key=True)
    deviceID: str = db.Column(db.String, db.ForeignKey(Sensor.deviceID), nullable=False, primary_key=True)
    measurement = db.Column(db.Text, nullable=False)
    timeStramp = db.Column(db.TIMESTAMP(True), nullable=False, primary_key=True)
