import subprocess
import os
import sys

home = sys.argv[1]

file = '[Desktop Entry]\nVersion=1.0\nName=YetiLevelOnePrimary\nExec=python3 '+home+'/yeticold/initialize.py YetiLevelOnePrimary %F\nTerminal=true\nX-MultipleArgs=false\nType=Application\nIcon='+home+'/yeticold/static/yeti.png\nStartupNotify=true'
subprocess.call('sudo echo "'+file+'" >> /usr/share/applications/YetiLevelOnePrimary.desktop', shell=True)
subprocess.call('sudo chmod +x /usr/share/applications/YetiLevelOnePrimary.desktop', shell=True)
# subprocess.run('sudo ln -s '+home+'/yeticold/shortcuts/YetiLevelOnePrimary.desktop '+home+'/Desktop/YetiLevelOnePrimary.desktop', shell=True, check=False)

