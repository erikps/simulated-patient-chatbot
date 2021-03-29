import asyncio
import atexit
import pathlib
import subprocess
import os
from util.util import get_venv_bin

FD = pathlib.Path(__file__).parent.absolute()


async def run_command(cmd, name, cwd):
    os.chdir(cwd)
    proc = await asyncio.create_subprocess_shell(' '.join(cmd), stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

    def terminate():
        proc.terminate()

    atexit.register(terminate)

    while True:
        stdout = await proc.stdout.read()
        stderr = await proc.stderr.read()
        if stdout:
            print(f'[{name}::stdout] {stdout.decode()}')

        if stderr:
            print(f'[{name}::stderr] {stderr.decode()}')


async def main():
    rasa_path = FD.joinpath('Chatbot-Rasa')
    webapp_path = FD.joinpath('simulated-patient-chatbot-frontend/webapp')
    server_path = FD.joinpath('simulated-patient-chatbot-frontend/server')

    print(str(get_venv_bin(server_path).joinpath('python')))
    await asyncio.gather(
        run_command(
            [str(get_venv_bin(rasa_path).joinpath('rasa')), 'run'], 'rasa', str(rasa_path)),
        run_command([str(get_venv_bin(rasa_path).joinpath('rasa')),
                    'run', 'actions'], 'rasa actions', str(rasa_path)),
        run_command(['npm', 'start'], 'npm', str(webapp_path)),
        run_command([str((get_venv_bin(server_path)).joinpath(
            'python')), 'app.py'], 'flask', str(server_path))
    )

if __name__ == '__main__':
    asyncio.ProactorEventLoop().run_until_complete(main())
