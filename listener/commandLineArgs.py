from argparse import ArgumentParser


def parse():
	parser = ArgumentParser(description='Python3 Tor Rootkit Listener')
	parser.add_argument('lport', type=int, help='The port the hidden service should listen on.')
	parser.add_argument('fport', type=int, help='The port the hidden service should forward to.')
	args = parser.parse_args()
	return args.lport, args.fport