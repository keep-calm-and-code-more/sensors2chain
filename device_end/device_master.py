import sqlite3
import time
import json
from sim7000 import submitData
from dht11 import getHT


timeInterval = 120  # 提交的时间间隔
table_name = "tilt"


def queryShiftCount():
    now = int(time.time() * 1000)
    left = now - timeInterval * 1000
    conn = sqlite3.connect("tilt.db")
    cur = conn.cursor()
    r = []
    for row in cur.execute("SELECT d FROM {} WHERE ts > ?".format(table_name), [left]):
        r.append(json.loads(row[0]))
    return r


if __name__ == '__main__':
    d = {}
    d["dht11"] = getHT()
    d["tilt"] = queryShiftCount()
    submitData(d, "159.226.5.116", "23300")
