from colorama import init, Fore
from colorama import Style as S


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
