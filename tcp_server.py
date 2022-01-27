from simpletcp.tcpserver import TCPServer


def echo(ip, queue, data):
    print(data)
    queue.put(b"echo ok")


server = TCPServer("public", 23300, echo)
server.run()
