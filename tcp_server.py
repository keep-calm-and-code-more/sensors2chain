from simpletcp.tcpserver import TCPServer
import peer_pb2 as peer

def echo(ip, queue, data):
    print(data)
    trans = peer.Transaction()
    trans.ParseFromString(data)
    print(trans)
    queue.put(b"echo ok")


server = TCPServer("public", 23300, echo)
server.run()
