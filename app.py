from flask import Flask, request

from twisted.internet.protocol import DatagramProtocol # Protocol for UDP connections
from twisted.internet import reactor


# app = Flask('innkeeper')
# 
# @app.route('/')
# def get_connected_devices():
#     pass

app = Flask(__name__)

available_ips = set()

@app.route('/', methods=["GET"])
def get_connected_devices():
    remote_addr = request.headers.get("X-Forwarded-For")
    # Al desplegarlo tiene varias IPs del forward que habrá que manejar
    # ('62.99.106.92, 188.114.111.49, 10.217.253.201, 10.217.119.222', 1)
    remote_addr = remote_addr.replace("('", "").split(',')[0]
    port = request.args.get('p', default = 1, type = int)
    addr = remote_addr, port
    print(f"New address received: {addr}")
    if addr not in available_ips:
        available_ips.add(addr)
    addresses = "\n".join([str(x) for x in available_ips])
    return f'{addresses}'

"""
class Server(DatagramProtocol):
    # El server sólo sirve para dar la lista de los addresses existentes en el chat
    def __init__(self):
        # Change set to 
        self.clients = set()

    def datagramReceived(self, datagram: bytes, addr):
        datagram = datagram.decode("utf-8")
        if datagram == "ready":
            addresses = "\n".join([str(x) for x in self.clients])

            self.transport.write(addresses.encode('utf-8'), addr)
            self.clients.add(addr)


    def run(self):
        app = Flask('innkeeper')
"""
# if __name__ == '__main__':
#     reactor.listenUDP(9999, Server())
#     reactor.run()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')