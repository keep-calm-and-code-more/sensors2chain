import shortuuid
from main import db
import db_models
from main import app

with app.app_context():

    db.create_all()
    a = db_models.Project(projectID="fXUkqzDUZmMGahdDLrnC5Q", name="桌面环境监测", remark="demo")

    db.session.add(db_models.Project(projectID=shortuuid.uuid(), name="2月27日运输监测监测", remark="测试数据project2"))
    a.devices.append(db_models.Device(deviceID="DEVICE_00"))
    db.session.add(a)
    db.session.add(db_models.Sensor(sensorType="温度传感器", deviceID="DEVICE_00"))
    db.session.add(db_models.Sensor(sensorType="湿度传感器", deviceID="DEVICE_00"))
    db.session.add(db_models.Sensor(sensorType="振动传感器", deviceID="DEVICE_00"))
    db.session.commit()
