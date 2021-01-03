import subprocess as sp


def executeShell(command) -> str:
	try:
		proc = sp.Popen(command, shell=True, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
		output = proc.stdout.read() + proc.stderr.read()
		output = output.decode()
	except subprocess.SubprocessError as error:
		return str(error)
	else:
		return output