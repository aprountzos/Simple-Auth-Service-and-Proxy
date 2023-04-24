import signal
import socket
import sys
import threading
import json
import requests
HOST = "127.0.0.5"  # Standard loopback interface address (localhost)
PORT = 65430
AUTH_URL = "http://127.0.0.1:8000/auth/token/verify/"
class Proxy:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.proxySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.proxySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.buffer_size = 4096
        signal.signal(signal.SIGINT, self.signal_handler)
        
    def signal_handler(self, sig, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

    def run(self):
        self.proxySocket.bind((self.host, self.port))
        self.proxySocket.listen()
        print(" * Proxy server is running on {}:{}".format(self.host, self.port))

        while True:
            conn, addr = self.proxySocket.accept()
            print(" => {}:{}".format(addr[0],addr[1]))
            t =  threading.Thread(target=self.process_request, args=(conn, ))
            t.start()

    def process_request(self, client):
        payload = client.recv(self.buffer_size)
        header = self.parse_head(payload)
        if self.authenticate(header):
            host_port = payload.decode().split("\r\n")[1].split(" ")[1]
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host = host_port.split(":")[0]
            server.connect((socket.gethostbyname(host), 80))
            server.sendall(payload)
            server_data = server.recv(self.buffer_size)
            # print(server_data)
            server.close()
        else:
            server_data =  b"HTTP/1.1 401 Unauthorized\n\nError: Unauthorized access!"
        client.sendall(server_data)
        client.close()





    def authenticate(self, header):
        if "aprproxy" not in header:
            return False
        else:
            token = header["aprproxy"]
            payload={'token': token}
            response = requests.request("POST", AUTH_URL, headers={}, data=payload)
            if response.status_code == 200:
                return True
            else:
                return False

    def parse_head(self, head_request):
        nodes = head_request.split(b"\r\n\r\n")
        heads = nodes[0].split(b"\r\n")
        headers = {}


        for head in heads:
            pieces = head.split(b": ")
            key = pieces.pop(0).decode("utf-8")
            if key.startswith("Connection: "):
                headers[key.lower()] = "close"
            else:
                headers[key.lower()] = b": ".join(pieces).decode("utf-8")
        # print(data["headers"])
        return headers
    
if __name__ == "__main__":
    proxy = Proxy(HOST, PORT)
    proxy.run()