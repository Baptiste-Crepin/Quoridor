import socket
from _thread import *
import sys
import threading

hostname = socket.gethostname()
server = socket.gethostbyname(hostname)
#server = "10.128.173.172"
port = 42069
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
DISCOVERY_MSG = b"SERVER_DISCOVERY_REQUEST"
dsock.bind(('0.0.0.0', 5555))  # Bind to all available network interfaces on port 12345
try:
    s.bind((server, port))



except socket.error as e:
    str(e)
    print(e)

s.listen(4)
print("server:on    status: awaiting connection")

def threaded_client(conn):
    conn.send(str.encode("connected"))
    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")
            if not data:
                print("connection error")
                break
            else:
                print("recieved: ", reply)
                print("sending: ", reply)

            conn.sendall(str.encode(reply))
        except:
            break

def handle_client_request(data, client_address):
    if data == DISCOVERY_MSG:
        print("incomming discovery packet from:", client_address)
        response = socket.inet_aton(client_address[0])  # Convert the server IP address to binary format
        dsock.sendto(DISCOVERY_MSG, client_address)

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
    conn, addr = s.accept()
    print("incomming connection from:", addr)
    start_new_thread(threaded_client, (conn,))