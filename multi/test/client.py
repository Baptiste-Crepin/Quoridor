import socket
from _thread import *
import pickle
import threading


DISCOVERY_MSG = b"SERVER_DISCOVERY_REQUEST"
class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.hostname = socket.gethostname()
        self.server = "socket.gethostbyname(self.hostname)"
        self.port = 42069

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.sendto(DISCOVERY_MSG, ('<broadcast>', 5555))
        self.sock.settimeout(5.0)  # Set a timeout of 5 seconds for waiting for responses
        self.servers = set()
        self.slist = []

        #print('pick a server(number)')
        #self.id = self.connect(int(input()))
        #print(self.id)
        #self.send('im connecting')

    def connect(self):
        result = []
        while True:
            print('in a while')
            try:
                data, addr = self.sock.recvfrom(1024)
                if DISCOVERY_MSG in data:
                    server_info = pickle.loads(data.replace(DISCOVERY_MSG, b""))
                    result.append(server_info)
                    print("Server info:", server_info)
                    self.servers.add(addr[0])
            except socket.timeout:
                break
        print("Available servers:")
        for server in self.servers:
            self.slist.append(server)

        print(self.slist)

        def connect_helper():
            print('pick a server(number)')
            addr = (self.slist[int(input())], self.port)
            print('Connecting ...')

            try:
                print('trying to connect')
                self.client.connect(addr)
                print('connected')
            except:
                print("connection error")
                result.append(None)
            if len(result) == 0:
                print("server not found")
            else:
                return result[0]
        t = threading.Thread(target=connect_helper)
        t.start()
        t.join(timeout=5.0)  # Wait for 5 seconds for the connection to complete


    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

test = Network()
test.connect()
#test.send(input("type a message"))


#while True:
#    print(test.send(input("type a message")))


