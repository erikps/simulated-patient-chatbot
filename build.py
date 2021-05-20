from util.util import *
import subprocess
import os
import shutil
import pathlib


FD = pathlib.Path(__file__).parent.absolute()
BUILDPATH = FD.joinpath('build')

FRONTEND_PATH = FD.joinpath('simulated-patient-chatbot-frontend')
BACKEND_PATH = FD.joinpath('Chatbot-Rasa')


def build():

    clean()

    os.mkdir(BUILDPATH)
    shutil.copytree(FRONTEND_PATH.joinpath('server'), BUILDPATH.joinpath(
        'frontend'), ignore=shutil.ignore_patterns('venv'))

    # create the frontend build
    subprocess.run(['npm', 'run', 'build'], shell=True,
                   cwd=str(FRONTEND_PATH.joinpath('webapp')))

    shutil.copytree(FRONTEND_PATH.joinpath('webapp/build'),
                    BUILDPATH.joinpath('frontend/static'))

    shutil.copytree(BACKEND_PATH, BUILDPATH.joinpath('backend'), ignore=shutil.ignore_patterns(
        '.git/', 'venv', 'models', 'tests', '*.db', '*.db-shm', '*.db-wal', '*.dot'))

    os.mkdir(BUILDPATH.joinpath('backend/models'))

    # find the latest model and copy it to the build dir
    with os.scandir(BACKEND_PATH.joinpath('models')) as dir_entries:
        latest_model = max(
            dir_entries, key=lambda entry: entry.stat().st_ctime)
        shutil.copyfile(latest_model.path, BUILDPATH.joinpath(
            'backend/models').joinpath(latest_model.name))

    shutil.make_archive('build', 'zip', root_dir=BUILDPATH)


def clean():
    shutil.rmtree(BUILDPATH)


if __name__ == '__main__':
    build()
