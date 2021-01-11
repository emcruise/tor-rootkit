from argparse import ArgumentParser


def parse():
	parser = ArgumentParser(description='Python3 Tor Rootkit Listener')
	parser.add_argument('hiddenServicePort', type=int, help='The port the hidden service should listen on.')
	parser.add_argument('localPort', type=int, help='The port the hidden service should forward to.')
	args = parser.parse_args()
	return args.hiddenServicePort, args.localPort