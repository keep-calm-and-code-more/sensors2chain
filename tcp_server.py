from simpletcp.tcpserver import TCPServer
import peer_pb2 as peer
from RCPython.Client import Client

def echo(ip, queue, data):
    print(data)
    trans = peer.Transaction()
    trans.ParseFromString(data)
    print(trans)
    client = Client()
    r = client.postTranByString(trans).text
    print(r)
    queue.put(b"submit ok")


server = TCPServer("public", 23300, echo)
server.run()
