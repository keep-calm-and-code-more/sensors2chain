import sqlite3
import time
import json
from sim7000 import sendPost
from iotdb_helper import beijingts, ip, port_, username_, password_
from iotdb.dbapi import connect
import json

time_interval = 45  # 提交的时间间隔
device_id = "root.rciot.pi_01"


def get_last_all():
    conn = connect(
        "127.0.0.1",
        port_,
        username_,
        password_,
        fetch_size=1024,
        zone_id="UTC+8",
        sqlalchemy_mode=False,
    )
    cursor = conn.cursor()
    cursor.execute("select last * from {}.*".format(device_id))
    last_all = cursor.fetchall()
    return last_all


if __name__ == "__main__":
    while True:
        last_all = get_last_all()
        tx_dict = {}
        tx_dict["deviceID"] = device_id
        records = []
        ts_sthfromsamesensor_dict = {}
        for item in last_all:
            ts_k = item[0]
            sensor_output_k = item[1].replace(device_id + ".", "")
            v = item[2]
            ts_sthfromsamesensor_dict.setdefault(ts_k, {})[sensor_output_k] = v
        for ts_k, v in ts_sthfromsamesensor_dict.items():
            records.append({"ts": ts_k, **v})
        tx_dict["records"] = records
        print(json.dumps(tx_dict, indent=4))
        sendPost(tx_dict, "http://124.16.137.94:19999/transaction/postTranByString","Sensors2Chain",1, "save_record")
        time.sleep(time_interval)
