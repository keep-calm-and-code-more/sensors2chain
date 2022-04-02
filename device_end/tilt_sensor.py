import RPi.GPIO as GPIO
import time
import json
import sqlite3

GPIO.setmode(GPIO.BCM)
INPUT_PIN = 27
GPIO.setup(INPUT_PIN, GPIO.IN)
timeInterval = 30  # 统计周期


conn = sqlite3.connect("tilt.db")
table_name = "tilt"


def createTable():
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS {}(ts INTEGER , d TEXT)".format(table_name))
    conn.commit()
    cur.close()


def saveShifCount(d):
    ts = d["ts_start"]
    dStr = json.dumps(d)
    cur = conn.cursor()
    cur.execute("INSERT INTO {} (ts, d) VALUES (?,?)".format(table_name),
                [ts, dStr])
    conn.commit()
    cur.close()


def getShiftCount():
    start_time = time.time()
    count_of_shift = 0
    oldtilt = 1
    while True:
        newtilt = GPIO.input(INPUT_PIN)
        if oldtilt != newtilt:
            count_of_shift += 1
        oldtilt = newtilt
        now = time.time()
        if (now - start_time) > timeInterval:
            d = {
                "ts_start": int(start_time * 1000), "ts_end": int(now * 1000), "#": count_of_shift
            }
            saveShifCount(d)
            count_of_shift = 0
            start_time = now
        # print(count_of_shift)
        time.sleep(0.2)


if __name__ == '__main__':
    createTable()
    getShiftCount()
