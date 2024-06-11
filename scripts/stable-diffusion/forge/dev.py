"""
stable-dffusion forge-ui dev.py, put it in the webui directory and run it by python,
have to set the PYTHONPATH to the system/python/Lib directory,
have to set the A1111_HOME to the root directory of the A1111
good luck
"""

import os
import subprocess

# import sys

# TODO change this please
A1111_HOME = "/path/to/A1111_HOME"

# environment.bat ==============================================

# Define the directory
DIR_CUR = os.path.dirname(os.path.realpath(__file__))
DIR_PARENT = os.path.dirname(DIR_CUR)
DIR = os.path.join(DIR_PARENT, 'system')

# Set PATH
os.environ['PATH'] = os.path.join(DIR, 'git', 'bin') + os.pathsep + \
                     os.path.join(DIR, 'python') + os.pathsep + \
                     os.path.join(DIR, 'python', 'Scripts') + os.pathsep + \
                     os.environ['PATH']

# Set PY_LIBS
os.environ['PY_LIBS'] = os.path.join(DIR, 'python', 'Scripts', 'Lib') + os.pathsep + \
                        os.path.join(DIR, 'python', 'Scripts', 'Lib', 'site-packages')

# Set PY_PIP
os.environ['PY_PIP'] = os.path.join(DIR, 'python', 'Scripts')

# Set PYTHONPATH
os.environ['PYTHONPATH'] = os.path.join(DIR, 'python', 'Lib')

# Set SKIP_VENV
os.environ['SKIP_VENV'] = '1'

# Set PIP_INSTALLER_LOCATION
os.environ['PIP_INSTALLER_LOCATION'] = os.path.join(DIR, 'python', 'get-pip.py')

# Set TRANSFORMERS_CACHE
os.environ['TRANSFORMERS_CACHE'] = os.path.join(DIR, 'transformers-cache')

# webui-user.bat ==========================================

# os.environ['PYTHON'] = ''
# os.environ['GIT'] = ''
# os.environ['VENV_DIR'] = ''
# os.environ['COMMANDLINE_ARGS'] = ''


os.environ['A1111_HOME'] = A1111_HOME
os.environ['VENV_DIR'] = f"{A1111_HOME}/python"

# Set command line arguments
COMMANDLINE_ARGS = [
    '--ckpt-dir', f"{A1111_HOME}/models/Stable-diffusion",
    '--vae-dir', f"{A1111_HOME}/models/vae",
    '--controlnet-dir', f"{A1111_HOME}/models/ControlNet",
    '--controlnet-preprocessor-models-dir', f"{A1111_HOME}/extensions/sd-webui-controlnet/annotator/downloads",
    '--hypernetwork-dir', f"{A1111_HOME}/models/hypernetworks",
    '--embeddings-dir', f"{A1111_HOME}/embeddings",
    '--lora-dir', f"{A1111_HOME}/models/Lora",
    '--port', '30001'
]
os.environ['COMMANDLINE_ARGS'] = ' '.join(COMMANDLINE_ARGS)

# webui.bat ==========================================

# Define environment variables
PYTHON = 'python'
GIT = os.getenv('GIT')
VENV_DIR = os.getenv('VENV_DIR') or os.path.join(os.getcwd(), 'venv')
SD_WEBUI_RESTART = 'tmp/restart'
ERROR_REPORTING = False

# Create tmp directory
os.makedirs('tmp', exist_ok=True)

# Check if Python can be launched
"""
try:
    subprocess.check_call([PYTHON, '-c', ''])
except subprocess.CalledProcessError:
    print("Couldn't launch python")
    sys.exit(1)
"""

# Check if pip is installed
"""
try:
    subprocess.check_call([PYTHON, '-m', 'pip', '--help'])
except subprocess.CalledProcessError:
    print("Couldn't install pip")
    sys.exit(1)
"""

# Create a virtual environment
if not os.path.exists(VENV_DIR):
    import venv

    venv.create(VENV_DIR, with_pip=True)

# Activate the virtual environment
activate_file = os.path.join(VENV_DIR, 'Scripts', 'activate_this.py')
# TODO: Check if this is necessary
if os.path.exists(activate_file):
    exec(open(activate_file).read(), {'__file__': activate_file})

if __name__ == "__main__":

    # noinspection PyUnresolvedReferences
    import launch

    # Check for acceleration
    ACCELERATE = os.getenv('ACCELERATE')
    if ACCELERATE == 'True':
        ACCELERATE = os.path.join(VENV_DIR, 'Scripts', 'accelerate.exe')
        if os.path.exists(ACCELERATE):
            subprocess.call([ACCELERATE, 'launch', '--num_cpu_threads_per_process=6', 'launch.py'])
        else:
            print("Accelerate not found")
    else:
        launch.main()
        # subprocess.call([PYTHON, 'launch.py'])

    # Check for restart
    if os.path.exists('tmp/restart'):
        raise "manually restart is a better choice"
        # launch.main()
        # subprocess.call([PYTHON, 'launch.py'])
