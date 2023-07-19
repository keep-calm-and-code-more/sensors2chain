import time
from iotdb_helper import beijingts, ip, port_, username_, password_
from iotdb.utils.IoTDBConstants import TSDataType, TSEncoding, Compressor
from iotdb.Session import Session

import RPi.GPIO as GPIO
import json
import sqlite3

GPIO.setmode(GPIO.BCM)
INPUT_PIN = 27
GPIO.setup(INPUT_PIN, GPIO.IN)
timeInterval = 15  # 统计周期


def tilt_sensor_worker():
    session = Session(ip, port_, username_, password_, fetch_size=1024, zone_id="UTC+8")
    session.open(False)
    device = "root.rciot.pi_01.tilt_sensor"
    session.set_storage_group(device)
    series_config = {
        "measurements": [
            "tilt_sensor_count_last_15s",
        ],
        "datatypes": [TSDataType.INT32 for i in range(1)],
    }
    session.create_aligned_time_series(
        device,
        series_config["measurements"],
        series_config["datatypes"],
        [TSEncoding.PLAIN for i in range(1)],
        [Compressor.SNAPPY for i in range(1)],
    )
    start_time = time.time()
    count_of_shift = 0
    oldtilt = GPIO.input(INPUT_PIN)
    while True:
        try:
            newtilt = GPIO.input(INPUT_PIN)
            if oldtilt != newtilt:
                count_of_shift += 1
                oldtilt = newtilt
                now = time.time()
                if (now - start_time) > timeInterval:
                    # d = {
                    #     "ts_start": int(start_time * 1000), "ts_end": int(now * 1000), "#": count_of_shift
                    # }
                    session.insert_aligned_record(
                        device,
                        beijingts(),
                        series_config["measurements"],
                        series_config["datatypes"],
                        [count_of_shift],
                    )
                    print("sent: {}".format(count_of_shift))
                    count_of_shift = 0
                    start_time = now
        except Exception as e:
            print("except: {}".format(type(e)))
            raise e
        finally:
            time.sleep(0.2)


if __name__ == "__main__":
    tilt_sensor_worker()
