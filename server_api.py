from flask import Flask, request

from twisted.internet.protocol import DatagramProtocol # Protocol for UDP connections
from twisted.internet import reactor

app = Flask(__name__)

available_ips = set()

@app.route('/', methods=["GET"])
def get_connected_devices():
    remote_addr = request.headers.get("X-Forwarded-For")
    remote_addr = remote_addr.replace("('", "").split(',')[0]
    port = request.args.get('p', default = 1, type = int)
    addr = remote_addr, port

    if addr not in available_ips:
        available_ips.add(addr)

    addresses = "\n".join([str(x) for x in available_ips])
    return f'{addresses}'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')