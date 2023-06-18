import pickle
import socket
import time
from typing import Any
from graphical.widgets.menu import Menu

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
            print("startVars : ", startVars)
            return startVars
        except socket.error as e:
            print("Error on connection")
            raise SystemExit from e

    def multiLaunch(self, fullScreen, startVars: list[int], clientListLen: int, host: bool, currentMenu: object) -> \
            tuple[bool,
    int]:
        try:
            serverMessage = self.connection.recv(4096)
            print("received:", serverMessage)
            unpickled_message = pickle.loads(serverMessage)
            print("unpickled : ", unpickled_message)
            if unpickled_message[0] != "lenConnected":
                print("starting game", startVars)
                self.connection.setblocking(True)
                self.createGame(self.connection, fullScreen, startVars, host, currentMenu)

                return True, clientListLen
            else:
                print("connected players = ", unpickled_message[1])
                return False, int(unpickled_message[1])

        except Exception:
            return False, clientListLen

    def roomState(self):
        try:
            serverMessage = self.connection.recv(4096)
            return pickle.loads(serverMessage)

        except Exception:
            return

    @staticmethod
    def createGame(connection: socket.socket, fullScreen, startVars: list[Any], host: bool, currentMenu: object):
        """ creates an instance of the class: MultiplayerGame passing the user's choices as parameters """
        print("Game infos:", startVars)
        num = int(startVars[0])
        width = startVars[1]
        nbBarrier = startVars[2]
        nbPlayer = startVars[3]
        nbBots = startVars[4]
        startingPlayer = startVars[5]
        board = MultiplayerGame(connection, fullScreen, width, nbBarrier,
                                nbPlayer, host, startingPlayer, nbBots, num)
        Menu.newMenu(currentMenu, board)

    @staticmethod
    def getSelfHost() -> str:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # Doesn't need to be reachable, it's used to make the OS determine the preferred outgoing IP interface
            s.connect(('10.255.255.255', 1))
            host = s.getsockname()[0]
        except Exception:
            host = '0.0.0.0'  # Listen on all available interfaces
        finally:
            s.close()
        return host
