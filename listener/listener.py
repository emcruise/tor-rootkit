#!/usr/bin/env python3
from network import ListenerSocket, Tor
from shell import ListenerShell
from shell_ui.style import Style
import commandLineArgs
import os
import sys

"""
The main class of the listener Package.
It handles all other modules of the listener package.
"""
class Listener(Style):
    def __init__(self):
        #self.checkRunningAsRoot()
        lport, fport = commandLineArgs.parse()
        torHS = Tor('listener', lport, fport)
        listenerSocket = ListenerSocket(fport)
        listenerSocket.start()
        shell = ListenerShell(listenerSocket)
        shell.run()

    """
    Check if the programm runs as root.
    """
    def checkRunningAsRoot(self):
        if os.getuid() != 0:
            self.negSysMsg('Please run as root.')
            sys.exit(1)


if __name__ == '__main__':
    Listener()
