# Tor Rootkit
A python3 standalone Windows 10 Rootkit. The networking works over tor hidden services.
The exe Rootkit-File contains the tor expert bundle, so no staged payload is needed.

## Installation

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
