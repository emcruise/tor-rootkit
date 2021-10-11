import socket
import threading
import sys
from shell_ui.style import *
import os
import subprocess as sp
import stem.process
import stat


class Tor(Style):
    """
    A class to handle the tor process,
    and the tor hidden service.
    """
    BASE_DIR = 'hidden_service'
    TORRC_PATH = os.path.join('hidden_service', 'torrc')
    TOR_SOCKS_PORT = 9200

    def __init__(self, name, lPort, fPort):
        self.name = name
        # listen and forward port configured in /etc/tor/torrc
        self.lPort = lPort
        self.fPort = fPort

        # create hidden service directory
        if not os.path.isdir(self.BASE_DIR):
            os.mkdir(self.BASE_DIR)
            # the owner has full permissions over dir
            # equivalent to chmod 700
            os.chmod(self.BASE_DIR, stat.S_IRWXU)

        ps = ProgressSpinner('Starting Tor Process')
        ps.start()
        self.launch()
        ps.stop()
        print()
        self.posSysMsg('Onion: {}'.format(self.get_onion_address()))

    def launch(self):
        try:
            self.torProcess = stem.process.launch_tor_with_config(
                config={
                    'SocksListenAddress': '127.0.0.1:{}'.format(self.TOR_SOCKS_PORT),
                    'SocksPort': '{}'.format(self.TOR_SOCKS_PORT),
                    'HiddenServiceDir': '{}'.format(self.BASE_DIR),
                    'HiddenServiceVersion': '3',
                    'HiddenServicePort': '{} 127.0.0.1:{}'.format(self.lPort, self.fPort)
                })
        except Exception as error:
            self.negSysMsg('Error while starting tor: {}'.format(error))
            sys.exit(1)

    def get_onion_address(self):
        with open(os.path.join(self.BASE_DIR, 'hostname'), 'r') as f:
            # remove \n from hostname file
            return f.read().rstrip()


class ListenerSocket(Style, threading.Thread):
    """
    A class to handle the listener socket.
    It also handles the en- and decoding and the network protocol.
    """
    MAX_CONNECTIONS = 10

    def __init__(self, port):
        threading.Thread.__init__(self)
        threading.Thread.daemon = True
        self.bindAddr = ('127.0.0.1', port)
        # <self.__sock> should not be accessed from outside the class.
        self.__sock = self.create()
        self.__clients = []

    def create(self) -> socket.socket:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # allow address reuse
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(self.bindAddr)
            sock.listen(self.MAX_CONNECTIONS)
        except socket.error as error:
            self.negSysMsg(error)
            sys.exit(1)
        else:
            self.posSysMsg('Created socket and bound to hidden service forward port')
            return sock

    def run(self):
        """
        The <start> method runs as a thread and endless.
        It handles all incoming client connections and stores the according
        client objects in <self.__clients>.
        """
        self.posSysMsg('Listening for clients')
        while True:
            try:
                clientObjects = self.__sock.accept()
                client = Client(clientObjects)
                self.__clients.append(client)
                self.clientConnectMsg()
            except socket.error as error:
                self.negSysMsg(error)
                sys.exit(1)

    def getClients(self):
        return self.__clients

    def getClient(self, index):
        try:
            return self.__clients[index]
        except IndexError:
            self.negSysMsg('Client Index out of range.')

    def delClient(self, index):
        try:
            del (self.__clients[index])
        except IndexError:
            self.negSysMsg('Client Index out of range.')


class Client(Style):
    """
    A class the handles the interaction between the listener and the client.
    It should NOT be accessed from outside the module.
    """

    def __init__(self, clientObjects):
        self.__conn, self.__addr = clientObjects

    def send(self, task, args):
        """
        The Listener always sends a dictionary containing,
        A task and a list of optional arguments.
        """
        try:
            data = {'task': task, 'args': args}
            data = str(data)
            self.__conn.send(data.encode('utf-8'))
        except socket.error as error:
            self.negSysMsg('Error while sending: {}'.format(error))
            sys.exit(1)
        else:
            self.posSysMsg('==> send {} bytes'.format(sys.getsizeof(data)))

    def receive(self, buffersize):
        """
        The client always sends back the output of the current task,
        and the current working directory as a dictionary.
        """
        try:
            data = self.__conn.recv(buffersize)
            if len(data) <= 0:
                return -1, -1
            # get length in bytes before unpacking data
            dataNumBytes = sys.getsizeof(data)
            # decode from bytes to string
            data = data.decode('utf-8')
            # decode from string to dictionary
            data = eval(data)
        except socket.error as error:
            self.negSysMsg('Error while receiving: {}'.format(error))
            self.__conn.close()
            return -1, -1
        else:
            self.posSysMsg('<== received {} bytes'.format(dataNumBytes))
            return data['output'], data['cwd']
