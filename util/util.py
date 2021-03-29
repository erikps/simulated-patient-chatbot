import os
import sys
import subprocess


def get_venv_bin(path):
    if (os.name == 'nt'):
        return path.joinpath('venv/Scripts')
    return path.joinpath('venv/bin')


def create_venv(cwd, name='venv'):
    """ Creates a new venv and returns the path to its python executable. """
    subprocess.run([sys.executable, '-m', 'venv', 'venv'], cwd=str(cwd))
    return get_venv_bin(cwd).joinpath('python')


def install_pip_requirements(executable, cwd):
    subprocess.run([str(executable), '-m', 'pip', 'install',
                    '-r', 'requirements.txt'], cwd=str(cwd))


def train(path):
    subprocess.run(
        [str(get_venv_bin(path).joinpath('rasa')), 'train'], cwd=str(path))


def install(path):
    """ Install both venv and pip requirements. """
    executable = create_venv(path)
    install_pip_requirements(executable, path)


def install_npm(path):
    subprocess.run(['npm', 'i'], shell=True, cwd=str(path))
