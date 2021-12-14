import PyInstaller.__main__
import requests
import os
import zipfile
import sys
from random import choice
from string import (
    ascii_lowercase,
    ascii_uppercase,
    digits
)


def get_tor_expert_bundle():
    # create directory for the tor expert bundle
    os.mkdir('torbundle')
    os.chdir('torbundle')

    # download tor expert bundle
    tor_url = 'https://www.torproject.org/dist/torbrowser/11.0.2/tor-win32-0.4.6.8.zip'
    file_data = requests.get(tor_url, allow_redirects=True)

    # write downloaded tor expert bundle
    try:
        file = open('tor.zip', 'wb')
        file.write(file_data.content)
    except Exception as error:
        print('[-] Error while writing tor expert bundle: {}'.format(error))
        sys.exit(1)
    else:
        print('[*] Wrote tor expert bundle to file')

    # unzip tor expert bundle
    file = zipfile.ZipFile('tor.zip')
    file.extractall('.')
    print("[*] Unpacked Tor expert bundle")

    # change directory back to \client
    os.chdir('..')


if __name__ == '__main__':
    # dont download everytime
    if not os.path.isdir('torbundle') and os.name == 'nt':
        get_tor_expert_bundle()

    encryption_key_charset = ascii_uppercase + ascii_lowercase + digits
    encryption_key = ''.join(choice(encryption_key_charset) for _ in range(16))

    pyinstaller_args = ['client.py', '--onefile', '--key={}'.format(encryption_key)]
    pyinstaller_args_windows = ['--add-data=torbundle;torbundle', '--upx-dir=upx-3.96-win64']
    pyinstaller_args_linux = ['--add-data=tor_linux:tor_linux', '--upx-dir=upx-3.96-amd64_linux/']
    if os.name == 'nt':
        pyinstaller_args += pyinstaller_args_windows
        PyInstaller.__main__.run(pyinstaller_args)
    else:
        pyinstaller_args += pyinstaller_args_linux
        PyInstaller.__main__.run(pyinstaller_args)
