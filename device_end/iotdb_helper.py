import datetime
import pytz
from iotdb.Session import Session
from iotdb.utils.IoTDBConstants import TSDataType, TSEncoding, Compressor


def beijingts():
    # 获取当前时间的 datetime 对象
    now = datetime.datetime.now()

    # 创建一个表示 +0800 时区的对象
    tz = pytz.timezone("Asia/Shanghai")

    # 将当前时间转换为 +0800 时区的时间
    local_now = tz.localize(now)

    # 将 +0800 时区的时间转换为 UTC 时间
    utc_now = local_now.astimezone(pytz.utc)

    # 获取 UTC 时间的时间戳（整数类型）
    timestamp = int(utc_now.timestamp() * 1000)
    return timestamp


class IOTDBhelper(object):
    def __init__(self, sensor_name_lst):
        ip = "127.0.0.1"
        port_ = "6667"
        username_ = "root"
        password_ = "root"
        self.dbname = "root.rciot.pi_01"
        self.sensor_name_lst = sensor_name_lst
        self.session = Session(
            ip, port_, username_, password_, fetch_size=1024, zone_id="UTC+8"
        )
        self.session.open(False)
        self.session.set_storage_group(self.dbname)
        for sensor_name in sensor_name_lst:
            ts_name = "{}.{}".format(self.dbname, sensor_name)
            self.session.create_time_series(
                ts_name, TSDataType.FLOAT, TSEncoding.PLAIN, Compressor.SNAPPY
            )
            print(
                "{} expecting True, checking result: ".format(ts_name),
                self.session.check_time_series_exists(ts_name),
            )

    def __del__(self):
        self.session.close()

    def insertData(self, ts, sensor_name, v, data_type=TSDataType.FLOAT):
        if(sensor_name in self.sensor_name_lst):
            session.insert_record(self.dbname, ts, [sensor_name], [data_type], [v])
        else:
            raise Exception("sensor_name not in list")

if __name__ == "__main__":

    ip = "127.0.0.1"
    port_ = "6667"
    username_ = "root"
    password_ = "root"
    session = Session(ip, port_, username_, password_, fetch_size=1024, zone_id="UTC+8")
    session.open(False)
    session.set_storage_group("root.rciot.pi_01")
    session.create_time_series(
        "root.rciot.pi_01.s_DHT22", TSDataType.FLOAT, TSEncoding.PLAIN, Compressor.SNAPPY
    )
    print(
        "root.rciot.pi_01.s_DHT22 expecting True, checking result: ",
        session.check_time_series_exists("root.rciot.pi_01.s_DHT22"),
    )

    session.insert_record(
        "root.rciot.pi_01", beijingts(), ["s_DHT22"], [TSDataType.FLOAT], [28.6]
    )

    # session.close()
