from BMP388 import BMP388
import time
from iotdb_helper import beijingts, ip, port_, username_, password_
from iotdb.utils.IoTDBConstants import TSDataType, TSEncoding, Compressor
from iotdb.Session import Session

def bmp388worker():
    bmp388 = BMP388()
    session = Session(ip, port_, username_, password_, fetch_size=1024, zone_id="UTC+8")
    session.open(False)
    device = "root.rciot.pi_01.bmp388"
    session.set_storage_group(device)
    series_config = {
        "measurements": [
            "bmp388_temperature",
            "bmp388_pressure",
            "bmp388_altitude"
        ],
        "datatypes": [TSDataType.FLOAT for i in range(3)],
    }
    session.create_aligned_time_series(
        device,
        series_config["measurements"],
        series_config["datatypes"],
        [TSEncoding.PLAIN for i in range(3)],
        [Compressor.SNAPPY for i in range(3)],
    )
    while True:
        try:
            r = bmp388.get_temperature_and_pressure_and_altitude()
            r = [i/100.0 for i in r]
            session.insert_aligned_record(
                device,
                beijingts(),
                series_config["measurements"],
                series_config["datatypes"],
                r,
            )
            print("sent: {} | {} | {}".format(*r))
        except Exception as e:
            print("except: {}".format(type(e)))
        finally:
            time.sleep(3)

if __name__ == "__main__":
    bmp388worker()