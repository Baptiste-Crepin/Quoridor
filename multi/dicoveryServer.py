import pickle
import socket
import time
from typing import Any

from multi.multiplayerClient import MultiplayerGame


class SearchServer():
    """this class is used to create the sockets for discovery and the server"""

    def __init__(self) -> None:
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.discoSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.discoSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.DISCOVERY_MSG = b"SERVER_DISCOVERY_REQUEST"

    def discover(self) -> list[dict[str, Any]]:
        """send a discovery message on broadcast to find potential hosts on the local network returns a list of
        lobby with"""
        self.discoSock.sendto(self.DISCOVERY_MSG, ('<broadcast>', 5555))
        # Set a timeout of 5 seconds for waiting for responses
        self.discoSock.settimeout(1.0)
        serverList = list[dict[str, Any]]()

        try:
            start_time = time.time()
            while time.time() - start_time < 3:

                data, _ = self.discoSock.recvfrom(1024)
                try:
                    server_info = pickle.loads(data)
                    serverList.append(server_info)
                    print("Server info:", server_info)
                except pickle.UnpicklingError:
                    print("Received a non-Python object.")

        except socket.timeout:
            print('request timed out / no server found')
        return list(serverList)

    def connect(self, ip: str, port: int) -> list[int]:
        """connects the socket """
        try:
            self.connection.connect((ip, port))
            print("Connection active")
            serverMessage = self.connection.recv(4096)
            startVars = pickle.loads(serverMessage)
            print("startvars : ", startVars)
            return startVars
        except socket.error:
            print("Erreur sur la connection")
            raise SystemExit

    def multiLaunch(self, startVars: list[int], clientListLen, host: bool) -> tuple:
        try:
            serverMessage = self.connection.recv(4096)
            print("recived:", serverMessage)
            unpickeled_message = pickle.loads(serverMessage)
            print("unpickeled : ", unpickeled_message)
            if unpickeled_message[0] != "lenConnected":
                print("starting game", startVars)
                self.connection.setblocking(True)
                self.createGame(self.connection, startVars, host)

                return True, clientListLen
            else:
                print("conected players = ", unpickeled_message[1])
                return False, int(unpickeled_message[1])


        except Exception as e:
            return False, clientListLen

    @staticmethod
    def createGame(connection: socket.socket, startVars: list[Any], host: bool):
        """ creates an instance of the class: MultiplayerGame passing the user's choices as parameters """
        print("Game infos:", startVars)
        num = int(startVars[0])
        width = startVars[1]
        nbBarrier = startVars[2]
        nbPlayer = startVars[3]
        nbBots = startVars[4]
        Game = MultiplayerGame(connection, width, nbBarrier, nbPlayer, host, nbBots, num)
        Game.mainLoop()

    def roomstate(self):
        try:
            serverMessage = self.connection.recv(4096)
            unpickeled_message = pickle.loads(serverMessage)
            return unpickeled_message

        except Exception:
            return
