# Tor Rootkit
[![Docker build test](https://github.com/emcruise/TorRootkit/actions/workflows/docker-test.yml/badge.svg)](https://github.com/emcruise/TorRootkit/actions/workflows/docker-test.yml)
[![Python3 style-linting](https://github.com/emcruise/TorRootkit/actions/workflows/linting.yml/badge.svg)](https://github.com/emcruise/TorRootkit/actions/workflows/linting.yml)

A Python 3 standalone Windows 10 / Linux Rootkit. The networking communications are established over the tor network.

## Disclaimer
Use for educational purposes only.

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
docker run -v $(pwd)/executables:/executables/ -it listener
```

3. Deploy the executables:
When the listener is up and running it generates a "executables" directory containing different payloads for different plattforms.
```
TorRootkit/
│    ...
└    executables/
```

## Features
- Standalone executable, including python interpreter and tor
- The executable has a size of ~13MB on Windows and ~7MB on Linux
- the whole communication works over tor hidden services which guarantees some degree of anonymity
- The Listener can handle multiple clients
- The Client auto reconnects when a unexpected closed connection occurs

## Upcoming Features
- [x] cross-plattform compatibility
- [ ] Up- and Download functionality
- [ ] Screenshots
- [ ] Keylogging
- [ ] Persistence

## How to use
### Listener Shell Commands
| Command | Explanation |
| ------- | ----------- |
| `help`  | Shows the help menu |
| `^C` or `exit` | Exits the shell |
| `list` | lists all connected clients with their according index |
| `select <index>` | start shell with client |

### Client Shell Commands
| Command | Explanation |
| ------- | ----------- |
| `help`  | Shows the help menu |
| `^C` or `exit` | Exits the client shell and returns to listener shell |
| `os <command>` | Executes a command in the clients shell and returns the output |
| `background` | Keeps the connection to a client and returns to listener

## Contribution
All contributions are appreciated.

## Credits
- [Tor](https://www.torproject.org/)
- [PyInstaller](https://www.pyinstaller.org/)
- [Colorama Font](https://pypi.org/project/colorama/)
- [PySocks](https://pypi.org/project/PySocks/)
- [Stem](https://stem.torproject.org/)

