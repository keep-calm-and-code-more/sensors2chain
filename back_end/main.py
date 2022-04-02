from flask import Flask
from flask import request
from flask import json
try:
    from db_models import db, Project, Device
except ImportError:
    from .db_models import db, Project, Device
from flask import abort


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb+mariadbconnector://root:root@192.168.2.76:3307/device?useUnicode=true&characterEncoding=utf-8&serverTimezone=Asia/Shanghai&useSSL=false'
db.init_app(app)


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


@app.route("/project", methods=["GET", "POST"])
def project():
    if request.method == "GET":
        pageSize = request.args.get("pageSize", 10)
        pageNum = request.args.get("pageNum", 1)
        projectID = request.args.get('id', None)
        if projectID is None:
            # 全部
            res = Project.query.limit(pageSize).offset((pageNum - 1) * pageNum).all()
        else:
            res = [Project.query.get(projectID)]
        return makeRespose(res)
    elif request.method == "POST":
        # 处理创建
        return makeRespose("")


@app.route("/device", methods=["GET", "POST", "PUT"])
def device():
    if request.method == "GET":
        pageSize = request.args.get("pageSize", 10)
        pageNum = request.args.get("pageNum", 1)
        projectID = request.args.get('projectID', None)
        if projectID is None:
            abort(403, "必须有projectID")
        deviceID = request.args.get('id', None)
        if deviceID is None:
            # 全部
            res = db.session.query(Device).limit(pageSize).offset((pageNum - 1) * pageNum).all()
            print(res)
        else:
            res = [Device.query.get(deviceID)]
        return makeRespose(res)


@ app.route("/sensor-record")
def sensorRecord():
    
    return makeRespose("sensor_records")
