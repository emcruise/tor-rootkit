import PyInstaller.__main__
import requests
import os
import zipfile


def getTorExpertBundle():
	# create directory for the tor expert bundle
	os.mkdir('torbundle')
	os.chdir('torbundle')
	
	# download tor expert bundle
	torURL = 'https://www.torproject.org/dist/torbrowser/10.0.7/tor-win32-0.4.4.6.zip'
	fileData = requests.get(torURL, allow_redirects=True)
	with open('tor.zip', 'wb') as file:
		file.write(fileData.content)
	
	# unzip tor expert bundle
	with zipfile.ZipFile('tor.zip') as file:
		file.extractall('.')
	
	# remove zip file
	if os.path.isfile('tor.zip'):
		os.remove('tor.zip')


# dont download everytime
if not os.path.isdir('torbundle'):
	getTorExpertBundle()


PyInstaller.__main__.run([
    'client.py',
    '--onefile',
    #'--noconsole',
    '--add-data=torbundle;torbundle'
])