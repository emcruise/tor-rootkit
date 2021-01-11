#!/usr/bin/env python3
from network import ListenerSocket, Tor
from shell import ListenerShell
from shell_ui.style import Style
import commandLineArgs
import os
import sys
import shell_ui.ascii_art


class Listener(Style):
    """
    The main class of the listener Package.
    It handles all other modules of the listener package.
    """

    def __init__(self):
        lport, fport = commandLineArgs.parse()
        self.torHS = Tor('listener', lport, fport)
        listenerSocket = ListenerSocket(fport)
        listenerSocket.start()
        shell = ListenerShell(listenerSocket)
        shell.run()

    def __del__(self):
        try:
            self.torHS.torProcess.terminate()
        except AttributeError:
            pass
        finally:
            self.negSysMsg('Exiting')


if __name__ == '__main__':
    Listener()
