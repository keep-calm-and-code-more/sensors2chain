from simpletcp.tcpserver import TCPServer
import peer_pb2 as peer
from rcpy import postTranByString


host = "127.0.0.1:9081"


def echo(ip, queue, data):
    print(data)
    trans = peer.Transaction()
    trans.ParseFromString(data)
    print(trans)
    r = postTranByString(host, trans).text
    print(r)
    queue.put(b"submit ok")


server = TCPServer("public", 23300, echo)
server.run()
