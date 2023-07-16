"""RepChain数据拉取

"""
import requests
import copy
import typing
import time
import json
from back_end.main import app, db
from back_end.db_models import SensorRecord
from datetime import datetime
import pdb
import pprint


pp = pprint.PrettyPrinter(depth=2)


def saveD(list_d):
    print("saving {}".format(len(list_d)))
    with app.app_context():
        for r in list_d:
            # SensorRecord.__table__.insert().prefix_with(' IGNORE').values(d)
            d = {}
            d["sensorType"] = r.sensorType
            d["deviceID"] = r.deviceID
            d["measurement"] = r.measurement
            d["timeStamp"] = r.timeStamp
            db.session.execute(SensorRecord.__table__.insert(prefixes=["IGNORE"], values=d))
            # pdb.set_trace()
            # pp.pprint(json.dumps(vars(d)))
        db.session.commit()
        db.session.close()


class BlockPuller(object):

    """RepChain数据拉取功能类

    Attributes:
        url (str): RepChain的web接口地址，默认为http://127.0.0.1:8081
    """

    def __init__(self, url: str = "http://127.0.0.1:9081", current_height: int = 0):
        self.url = url
        self.current_height = current_height
        self.block_list = []

    @staticmethod
    def __getJSON(url: str) -> dict:
        """从web接口获取JSON数据，其返回结果为字典

        Args:
            url (str): 接口地址

        Returns:
            dict: Description
        """
        r = requests.get(url)
        data = r.json()
        return data

    def getChainInfo(self) -> dict:
        """获取chaininfo接口的数据，包括当前最大块高度等属性

        Returns:
            TYPE: Description
        """
        data = self.__getJSON("{}/chaininfo".format(self.url))
        return data

    def getOneBlock(self, height_index) -> dict:
        """获取一个区块的JSON数据

        Args:
            height_index (TYPE): Description

        Returns:
            TYPE: Description
        """
        data = self.__getJSON("{}/block/{}".format(self.url, height_index))
        return data

    def getBlocks(self, height_index_list: typing.Iterable) -> list:
        """获取多个区块数据的JSON数据，以列表形式返回

        Args:
            height_index_list (typing.Iterable): Description

        Returns:
            TYPE: Description
        """
        print("getBlocks height_index_list:")
        print(height_index_list)
        r = list(map(self.getOneBlock, height_index_list))
        # pp.pprint(r[2])
        return r

    def sync(self):
        """同步至当前最大区块高度，获取跨越的这些区块

        Returns:
            TYPE: Description
        """
        height: int = int(self.getChainInfo()["result"]["height"])  # 当前最大区块高度
        if not self.current_height == height:
            block_list = self.getBlocks(range(self.current_height + 1, height + 1))
            self.current_height = height
            self.block_list.extend(block_list)
            print("puller block_list size: {}".format(len(self.block_list)))


def parseBlock(item):
    inner_item = item['result']
    inner_item['height'] = int(inner_item['height'])
    return inner_item


def extractTransactionList(block_list) -> list:
    transaction_list = []
    success_set = set()
    for b in block_list:
        transactionResults = b["transactionResults"]
        for r in transactionResults:
            if not r["result"]:  # 如果result里面没东西则添加到成功set
                success_set.add(r["txId"])
        for tx in b["transactions"]:
            tx["inBlockHeight"] = b["height"]
            assert isinstance(tx["inBlockHeight"], int)
            transaction_list.append(tx)
    return transaction_list, success_set


def parseArg(tx):
    if (
        ("CHAINCODE_INVOKE" == tx["type"])
        and ("ContractAssetsTPL" == tx["cid"]["chaincodeName"])
        and ("putProof" == tx["ipt"]["function"])
    ):
        args_json = json.loads(tx["ipt"]["args"][0])
        content = {}
        content["inTransactionID"] = tx["id"]
        content["properties_body"] = args_json
        return content


def tsParser(ts):
    return datetime.fromtimestamp(ts / 1000.0)


def extractRecordList(transaction_list) -> list:
    arg_list = [parseArg(tx) for tx in transaction_list]
    print("extractRecordList/arg_list length:", len(arg_list))
    arg_list = [i for i in arg_list if i is not None]
    record_list = []
    for rawitem in arg_list:
        item = rawitem["properties_body"]
        try:
            record_list.append(SensorRecord(sensorType="温度传感器", deviceID="DEVICE_00", measurement=item["dht11"]["T"], timeStamp=tsParser(item["dht11"]["ts"])))
            record_list.append(SensorRecord(sensorType="湿度传感器", deviceID="DEVICE_00", measurement=item["dht11"]["H"], timeStamp=tsParser(item["dht11"]["ts"])))
            tilt_record_list = item["tilt"]
            for r in tilt_record_list:
                record_list.append(SensorRecord(sensorType="振动传感器", deviceID="DEVICE_00", measurement=json.dumps(r), timeStamp=tsParser(r["ts_end"])))
        except Exception as e:
            print(e)
            pdb.set_trace()
    return record_list


def someBlockParserRun(block_list):
    block_list = copy.deepcopy(block_list)
    block_list = [parseBlock(item) for item in block_list]
    transaction_list, success_set = extractTransactionList(block_list)
    print(len(transaction_list))
    filtered_transaction_list = [t for t in transaction_list if t["id"] in success_set]
    print(len(filtered_transaction_list))
    record_list = extractRecordList(filtered_transaction_list)
    print(len(record_list))
    return (block_list, transaction_list, record_list)


def saveBlockList(puller):
    pheight = puller.current_height
    print("Syncing, current height:{}".format(pheight))
    puller.sync()
    print("Synced, current height:{}".format(puller.current_height))
    # 将block_list中的时间等字段解析后存入mongodb
    if pheight == puller.current_height:
        print("No more new data.")
        return
    block_list, transaction_list, data_list = someBlockParserRun(puller.block_list[pheight:puller.current_height])
    saveD(data_list)
    return


if __name__ == '__main__':
    puller = BlockPuller()
    try:
        while True:
            saveBlockList(puller)
            time.sleep(10)  # 10秒取一次
    except KeyboardInterrupt:
        print('interrupted!')
