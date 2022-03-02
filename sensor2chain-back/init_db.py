import shortuuid
from main import db
import db_models
from main import app

with app.app_context():

    db.create_all()
    a = db_models.Project(projectID=shortuuid.uuid(), name="仓库书画监测", remark="测试数据project1")

    db.session.add(db_models.Project(projectID=shortuuid.uuid(), name="2月27日运输监测监测", remark="测试数据project2"))

    a.devices.append(db_models.Device(deviceID="device011"))
    db.session.add(a)
    b = db_models.Sensor(sensorType="Temperature", deviceID="device011")
    db.session.add(b)
    db.session.commit()
