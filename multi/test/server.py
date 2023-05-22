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

print("server:on    status: awaiting connection")

lobbyInfo = {'ip': server,
             'port': 45678,
             'lobbyName': "lobby de toto"
             }
def threaded_client(conn):
    conn.send(str.encode("connected"))
    reply = ""
    while True:
        try:
            data = conn.recv(2048)

        except:
            break

def handle_client_request(data, client_address):
    if data == DISCOVERY_MSG:
        print("incomming discovery packet from:", client_address)
        response = pickle.dumps(lobbyInfo)  # Convert the server IP address to binary format
        dsock.sendto(response, client_address)
        print("handeling request")

def handle_incoming_requests():
    while True:
        data, client_address = dsock.recvfrom(1024)
        client_thread = threading.Thread(target=handle_client_request, args=(data, client_address))
        client_thread.start()


incoming_thread = threading.Thread(target=handle_incoming_requests)
incoming_thread.start()



while True:
    data, addre = dsock.recvfrom(1024)
    if data == DISCOVERY_MSG:
        print("incomming discovery packet from:", addre)
        dsock.sendto(DISCOVERY_MSG, addre)