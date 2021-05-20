import shutil
import os
import requests

BACKEND_PATH = './srv/backend'
FRONTEND_PATH = './srv/frontend'
STATIC_PATH = './srv/var/www/static'

TMP_BUILDPATH = '__build_tmp'
TMP_BUILDPATH_ZIP = TMP_BUILDPATH + '.zip'

def download_zip(url, filepath):
    request = requests.get(url, stream=True)
    with open(filepath, 'wb') as f:
        for chunk in request.iter_content(chunk_size=128):
            f.write(chunk)


if __name__ == '__main__':
    try:
        shutil.rmtree(BACKEND_PATH)
        shutil.rmtree(FRONTEND_PATH)
        shutil.rmtree(STATIC_PATH)
    except Exception as e:
        print(e)

    download_zip(
        'https://github.com/erikps/simulated-patient-chatbot/releases/latest/download/build.zip', TMP_BUILDPATH_ZIP)
    shutil.unpack_archive(TMP_BUILDPATH_ZIP, './' + TMP_BUILDPATH)

    shutil.copytree(TMP_BUILDPATH + '/backend/', BACKEND_PATH)
    shutil.move(TMP_BUILDPATH + '/frontend/static', STATIC_PATH)
    shutil.copytree(TMP_BUILDPATH + '/frontend/', FRONTEND_PATH)

    shutil.rmtree(TMP_BUILDPATH)
    os.remove(TMP_BUILDPATH_ZIP)

    print(
        """NOTE: You may need to updates the virtual environments in '/srv/venvs', if python dependencies have changed. 
        To do so, run '/srv/venvs/backned/bin/pip install -r /srv/backend/requirements.txt' and the equivalent command for 'frontend'. 
        Furthermore, please note that this script did not update any nginx or systemd configuration files that may have changed.
        """)
