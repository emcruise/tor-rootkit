from colorama import init, Fore
from colorama import Style as S
from sys import stdout


class Style:
    """
    The style class of the listener package.
    It is designed to work as a superclass for all other package classes.
    """

    def __init__(self):
        # initialize colored Font
        init()

    def posSysMsg(self, string):
        print('[' + Fore.GREEN + '*' + S.RESET_ALL + '] ' + string)

    def negSysMsg(self, string):
        print('[' + Fore.RED + '-' + S.RESET_ALL + '] ' + string)

    def clientConnectMsg(self):
        # Dont print any client address info since the connection works over
        # tor hidden services and the address info would be about the exit node.
        stdout.write('\n[' + Fore.GREEN + '*' + S.RESET_ALL + '] ' + 'Client connected to the server' + '\nlistener > ')
