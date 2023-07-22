import multiprocessing
from bmp388worker import bmp388worker
from dht11worker import dht11worker
from flame_sensor_worker import flame_sensor_worker
from infrared_temperature_sensor_worker import infrared_temperature_sensor_worker
from light_sensor_worker import light_sensor_worker
from mpu6050worker import mpu6050worker
from mq5_gas_sensor_worker import mq5_gas_sensor_worker
from sgp40worker import sgp40worker
from tilt_sensor_worker import tilt_sensor_worker
from uv_sensor_worker import uv_sensor_worker


all_worker = [bmp388worker, dht11worker, flame_sensor_worker, infrared_temperature_sensor_worker, light_sensor_worker, mpu6050worker, mq5_gas_sensor_worker, sgp40worker, tilt_sensor_worker, uv_sensor_worker]

if __name__ == '__main__':
    # 创建子进程
    for worker in all_worker:
        p = multiprocessing.Process(target=worker)
        p.start()