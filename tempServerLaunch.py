import subprocess
import sys

if __name__ == "__main__":

    python_path = sys.executable

    server_process = subprocess.Popen([python_path, 'multiplayerServer.py'])
    client_process = subprocess.Popen([python_path, 'multiplayerClient.py'])

    server_process.wait()
    client_process.wait()
