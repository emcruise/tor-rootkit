from colorama import init, Fore, Style


def draw():
    init()
    # Source: http://patorjk.com/software/taag/#p=display&f=Graffiti&t=TorRootkit
    print('___________         __________               __   __   .__  __   ')
    print('\\__    ___/_________\\______   \\ ____   _____/  |_|  | _|__|/  |_ ')
    print('  |    | /  _ \\_  __ \\       _//  _ \\ /  _ \\   __\\  |/ /  \\   __\\')
    print('  |    |(  <_> )  | \\/    |   (  <_> |  <_> )  | |    <|  ||  |  ')
    print('  |____| \\____/|__|  |____|_  /\\____/ \\____/|__| |__|_ \\__||__|  ')
    print('                            \\/                        \\/         ')
    print(Fore.GREEN + Style.BRIGHT + 'by emcruise' + Style.RESET_ALL)