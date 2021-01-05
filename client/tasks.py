import subprocess as sp


def executeShell(command) -> str:
	try:
		return sp.getoutput(command)
	except sp.SubprocessError as error:
		return str(error)