import time
from iotdb_helper import beijingts, ip, port_, username_, password_
from iotdb.utils.IoTDBConstants import TSDataType, TSEncoding, Compressor
from iotdb.Session import Session

import RPi.GPIO as GPIO
import json
import sqlite3
from device_master import device_id
from iotdb_helper import suppress_err, restore_err

GPIO.setmode(GPIO.BCM)
INPUT_PIN = 27
GPIO.setup(INPUT_PIN, GPIO.IN)


def getTile(timeInterval=15):
    start_time = time.time()
    now = start_time
    count_of_shift = 0
    oldtilt = GPIO.input(INPUT_PIN)
    while True:
        try:
            if (now - start_time) > timeInterval:
                return count_of_shift
            newtilt = GPIO.input(INPUT_PIN)
            if oldtilt != newtilt:
                count_of_shift += 1
                oldtilt = newtilt
        except Exception as e:
            print("except: {}".format(type(e)))
            raise e
        finally:
            now = time.time()
            time.sleep(0.2)


def tilt_sensor_worker():
    session = Session(ip, port_, username_, password_, fetch_size=1024, zone_id="UTC+8")
    session.open(False)
    device = device_id + ".tilt_sensor"
    out = suppress_err()
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
    restore_err(out)
    while True:
        count_of_shift = getTile()
        session.insert_aligned_record(
            device,
            beijingts(),
            series_config["measurements"],
            series_config["datatypes"],
            [count_of_shift],
        )
        print("---倾角传感器记录: {}".format(count_of_shift))


if __name__ == "__main__":
    tilt_sensor_worker()
