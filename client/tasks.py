import subprocess as sp
import os


def execute_shell(command) -> str:
    # cant change directory in a subprocess
    if command[:2] == 'cd':
        try:
            os.chdir(command[3:])
            return ''
        except Exception as error:
            return str(error)
    # if the command is not "cd" execute subprocess
    try:
        return sp.getoutput(command)
    except sp.SubprocessError as error:
        return str(error)
