from colorama import init, Fore
from colorama import Style as S
from sys import stdout
from time import sleep
from threading import Thread
from progress.spinner import Spinner


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


class ProgressSpinner(Thread):
    def __init__(self, message):
        Thread.__init__(self)
        Thread.daemon = True
        self.message = message

    def run(self):
        self.running = True
        spinner = Spinner('[' + Fore.GREEN + '*' + S.RESET_ALL + '] ' + '{} '.format(self.message))
        while self.running:
            spinner.next()
            sleep(0.2)

    def stop(self):
        self.running = False