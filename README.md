# Tor Rootkit
**The Rootkit is still under production and not completely working yet.**

A python3 standalone Windows 10 Rootkit. The networking works over tor hidden services.
The exe Rootkit-File contains the tor expert bundle, so no staged payload is needed.

## Installation
First clone the git repository and change directory into the repo.

### Listener
Note: The Listener is desgined to run on linux.
In order for the listener to work you need to configure a Tor Hidden Service in /etc/tor/torrc,
with the base directory being /var/lib/tor.

After that the listener can be run with:
```bash
sudo python listener.py <listen-port> <forward-port>
```

### Client
Note: The compilation of the Rootkit client ONLY works on Windows. 

Install all dependencies:
```bash
pip3 install -r client\requirements.txt
```
Once the dependencies are installed you can build the executable file:
```bash
python client\build.py
```
The .exe file should now be at:
```bash
.\client\dist\client.exe
```

## Features
- Standalone executable, including python interpreter and tor expert bundle (~13MB)
- the whole communication works over tor hidden services which guarantees some degree of anonymity
