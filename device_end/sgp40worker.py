from SGP40 import SGP40
from sensirion_gas_index_algorithm.voc_algorithm import VocAlgorithm
import time
from iotdb_helper import beijingts, ip, port_, username_, password_
from iotdb.utils.IoTDBConstants import TSDataType, TSEncoding, Compressor
from iotdb.Session import Session
from device_master import device_id
from iotdb_helper import  suppress_err, restore_err

def sgp40worker():
    sgp = SGP40()
    voc_algorithm = VocAlgorithm()
    time.sleep(0.5)
    session = Session(ip, port_, username_, password_, fetch_size=1024, zone_id="UTC+8")
    session.open(False)
    device = device_id + ".sgp40"
    out = suppress_err()
    session.set_storage_group(device)
    series_config = {
        "measurements": [
            "sgp40_voc_raw",
            "sgp40_voc_index",
        ],
        "datatypes": [TSDataType.INT64, TSDataType.FLOAT],
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
            # print("Raw Gas: ", sgp.raw())
            s_voc_raw = sgp.measureRaw(27, 45)
            voc_index = voc_algorithm.process(s_voc_raw)  # 1-500
            session.insert_aligned_record(
                device,
                beijingts(),
                series_config["measurements"],
                series_config["datatypes"],
                [s_voc_raw, voc_index],
            )
            print("---SGP40传感器记录: {} | {}".format(s_voc_raw, voc_index))
        except Exception as e:
            print("except: {}".format(type(e)))
        finally:
            time.sleep(1)  # voc算法明确要求1s


if __name__ == "__main__":
    sgp40worker()
