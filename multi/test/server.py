import socket
from _thread import *
import sys
import threading
import pickle

hostname = socket.gethostname()
server = socket.gethostbyname(hostname)


dsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
DISCOVERY_MSG = b"SERVER_DISCOVERY_REQUEST"
dsock.bind(('0.0.0.0', 5555))  # Bind to all available network interfaces on port 12345



lobbyInfo = {'discoverymessage': DISCOVERY_MSG,
             'ip': server,
             'port': 45678,
             'lobbyName': "lobby de toto"
             }
def handle_client_request(data, client_address):
    if data == DISCOVERY_MSG:
        print("incomming discovery packet from:", client_address)
        response = pickle.dumps(lobbyInfo)  # Convert the server IP address to binary format
        dsock.sendto(response, client_address)
        print("handeling request")

def discoveryServer():
    while True:
        data, addre = dsock.recvfrom(1024)
        handle_client_request(data, addre)



