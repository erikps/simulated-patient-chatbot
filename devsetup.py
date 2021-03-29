import pip
import os
import subprocess
import sys
import pathlib
import argparse
from util.util import *

# The file directory
FD = pathlib.Path(__file__).parent.absolute()


def check_requirements():
    """ Ensure that the appropriate versions of python and pip are installed. """
    if not (sys.version_info.major == 3 and sys.version_info.minor == 7):
        print('Please use python version 3.7.')
        exit(-1)

    (pip_major_v, pip_minor_v, _) = tuple(map(int, pip.__version__.split('.')))

    if pip_major_v > 20 or (pip_major_v == 20 and pip_minor_v > 2):
        print(
            """
            Using incompatible pip version. Please use pip version 20.2 or lower. \n
            To downgrade the pip version run 'python -m pip install --upgrade pip==20.2'.
            """
        )
        exit(-1)


def main(should_train):
    install(FD.joinpath('Chatbot-Rasa'))

    if should_train:
        train(FD.joinpath('Chatbot-Rasa'))

    install(FD.joinpath('simulated-patient-chatbot-frontend/server'))
    install_npm(FD.joinpath('simulated-patient-chatbot-frontend/webapp'))


if __name__ == '__main__':
    check_requirements()

    parser = argparse.ArgumentParser()
    parser.add_argument('--train', action='store_true')
    args = parser.parse_args()

    main(args.train)
