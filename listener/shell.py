from style import Style

"""
Handles all the user input for the listener shell.
"""
class ListenerShell(Style):
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
                    data, _ = client.receive()
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
    def __init__(self, client):
        self.client = client

    def run(self):
        