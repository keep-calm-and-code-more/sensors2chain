from MLX90614 import MLX90614
import time
from iotdb_helper import beijingts, ip, port_, username_, password_
from iotdb.utils.IoTDBConstants import TSDataType, TSEncoding, Compressor
from iotdb.Session import Session
from device_master import device_id
from iotdb_helper import suppress_err, restore_err


def infrared_temperature_sensor_worker():
    sensor = MLX90614()
    session = Session(ip, port_, username_, password_, fetch_size=1024, zone_id="UTC+8")
    session.open(False)
    device = device_id + ".infrared_temperature_sensor"
    out = suppress_err()
    session.set_storage_group(device)
    series_config = {
        "measurements": [
            "infrared_temperature_sensor_ambient_temp",
            "infrared_temperature_sensor_object_temp",
        ],
        "datatypes": [TSDataType.FLOAT for i in range(2)],
    }
    session.create_aligned_time_series(
        device,
        series_config["measurements"],
        series_config["datatypes"],
        [TSEncoding.PLAIN for i in range(2)],
        [Compressor.SNAPPY for i in range(2)],
    )
    restore_err(out)
    while True:
        try:
            amb_obj_temp = (
                round(sensor.get_amb_temp(), 2),
                round(sensor.get_obj_temp(), 2),
            )
            session.insert_aligned_record(
                device,
                beijingts(),
                series_config["measurements"],
                series_config["datatypes"],
                [amb_obj_temp[0], amb_obj_temp[1]],
            )
            print(
                "---非接触式红外温度传感器记录: {} | {}".format(
                    amb_obj_temp[0], amb_obj_temp[1]
                )
            )
        except Exception as e:
            print("except: {}".format(type(e)))
        finally:
            time.sleep(3)


if __name__ == "__main__":
    infrared_temperature_sensor_worker()
