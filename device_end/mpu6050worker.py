from mpu6050 import mpu6050
# import json
from iotdb_helper import beijingts, ip, port_, username_, password_
from iotdb.utils.IoTDBConstants import TSDataType, TSEncoding, Compressor
from iotdb.Session import Session
import time

def mpu6050worker():
    """加速度传感器，需要主动读取"""
    session = Session(ip, port_, username_, password_, fetch_size=1024, zone_id="UTC+8")
    session.open(False)
    device = "root.rciot.pi_01.mpu6050"
    session.set_storage_group(device)
    series_config = {
        "measurements": [
            "mpu6050_x",
            "mpu6050_y",
            "mpu6050_z",
            "mpu6050_gyro_x",
            "mpu6050_gyro_y",
            "mpu6050_gyro_z",
            "mpu6050_temperature",
        ],
        "datatypes": [TSDataType.FLOAT for i in range(7)],
    }
    session.create_aligned_time_series(
        device,
        series_config["measurements"],
        series_config["datatypes"],
        [TSEncoding.PLAIN for i in range(7)],
        [Compressor.SNAPPY for i in range(7)],
    )
    sensor = mpu6050(0x68)
    while True:
        try:
            accelerometer_data = sensor.get_accel_data()
            gyro_data = sensor.get_gyro_data()
            temperature = sensor.get_temp()
            session.insert_aligned_record(
                device,
                beijingts(),
                series_config["measurements"],
                series_config["datatypes"],
                [
                    accelerometer_data["x"],
                    accelerometer_data["y"],
                    accelerometer_data["z"],
                    gyro_data["x"],
                    gyro_data["y"],
                    gyro_data["z"],
                    temperature,
                ],
            )
            print(
                "sent: {} | {} | {}".format(accelerometer_data, gyro_data, temperature)
            )
        except Exception as e:
            print("except: {}".format(type(e)))
        finally:
            time.sleep(3)


if __name__ == "__main__":
    mpu6050worker()
