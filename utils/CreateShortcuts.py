import subprocess
import os

home = os.getenv("HOME")

file = '[Desktop Entry]\nVersion=1.0\nName=YetiLevelOnePrimary\nExec=python3 '+home+'/yeticold/initialize.py YetiLevelOnePrimary %F\nTerminal=false\nX-MultipleArgs=false\nType=Application\nIcon='+home+'/yeticold/static/logo.png\nStartupNotify=true'
subprocess.call('sudo echo "'+file+'" >> /usr/shared/applications/YetiLevelOnePrimary.desktop', shell=True)
subprocess.call('sudo chmod +x /usr/shared/applications/YetiLevelOnePrimary.desktop', shell=True)
subprocess.run('ln -s ~/yeticold/shortcuts/YetiLevelOnePrimary.desktop ~/Desktop/YetiLevelOnePrimary.desktop', shell=True, check=False)

