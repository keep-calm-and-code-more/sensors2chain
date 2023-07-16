from flask import Flask
from flask import request
from flask import json
try:
    from db_models import db, Project, Device, SensorRecord
except ImportError:
    from .db_models import db, Project, Device, SensorRecord
from flask import abort
import pdb


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@192.168.2.76:3306/device?charset=utf8'
db.init_app(app)
fx = {"DESC": db.desc, "ASC": db.asc}


def makeRespose(res, count, code: int = 0, msg: str = "ok"):
    json_r = json.dumps(
        {"code": code, "msg": msg, "data": {"list": res, "count": count}},
        ensure_ascii=False,
    )
    print(json_r)
    return app.response_class(
        response=json_r,
        mimetype="application/json",
    )


@app.route("/project", methods=["GET", "POST"])
def project():
    if request.method == "GET":
        pageSize = int(request.args.get("pageSize", 10))
        pageNum = int(request.args.get("pageNum", 1))
        projectID = request.args.get('id', None)
        sortField = request.args.get("sortField", "projectID")
        order = request.args.get("order", "ASC")
        if projectID is None:
            # 全部
            res = Project.query.order_by(fx[order](sortField)).limit(pageSize).offset((pageNum - 1) * pageNum).all()
            return makeRespose(res, Project.query.count())
        else:
            res = [Project.query.get(projectID)] if Project.query.get(projectID) else []
            return makeRespose(res, len(res))
    elif request.method == "POST":
        # 处理创建
        pass
        return makeRespose("")


@app.route("/device", methods=["GET", "POST", "PUT"])
def device():
    if request.method == "GET":
        pageSize = int(request.args.get("pageSize", 10))
        pageNum = int(request.args.get("pageNum", 1))
        projectID = request.args.get('projectID', None)
        sortField = request.args.get("sortField", "deviceID")
        order = request.args.get("order", "ASC")
        if projectID is None:
            abort(403, "必须有projectID")
        deviceID = request.args.get('id', None)
        if deviceID is None:
            # 全部
            res = db.session.query(Device).order_by(fx[order](sortField)).limit(pageSize).offset((pageNum - 1) * pageNum).all()
            print(res)
        else:
            res = [Device.query.get(deviceID)] if Device.query.get(deviceID) else []
        return makeRespose(res, db.session.query(Device).count())


def sensorRecordMapper(r: SensorRecord) -> dict:
    d = {}
    d["sensorType"] = r.sensorType
    d["deviceID"] = r.deviceID
    d["measurement"] = r.measurement
    d["timeStamp"] = r.timeStamp.strftime("%Y-%m-%d %H:%M:%S")
    return d


@app.route("/sensor-record", methods=["GET"])
def sensorRecord():
    mapping = {"UPDATE_TIME": "timeStamp"}
    deviceID = request.args.get('deviceID', None)
    pageSize = int(request.args.get("pageSize", 10))
    pageNum = int(request.args.get("pageNum", 1))
    sortField = request.args.get("sortField", "timeStamp")
    sensorType = request.args.get("sensorType", None)
    if sortField in mapping:
        sortField = mapping[sortField]
    order = request.args.get("order", "DESC")
    if deviceID is None:
        abort(403, "必须有deviceID")
    else:
        if sensorType:
            q = db.session.query(SensorRecord).order_by(fx[order](sortField)).filter_by(deviceID=deviceID, sensorType=sensorType)
        else:
            q = db.session.query(SensorRecord).order_by(fx[order](sortField)).filter_by(deviceID=deviceID)
        res = q.limit(pageSize).offset((pageNum - 1) * pageNum).all()
        count = db.session.query(SensorRecord).filter_by(deviceID=deviceID).count()
        res = list(map(sensorRecordMapper, res))
        return makeRespose(res, count)
