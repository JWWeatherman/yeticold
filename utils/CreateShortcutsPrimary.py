import subprocess
import os
import sys

home = sys.argv[1]

file = '[Desktop Entry]\nVersion=1.0\nName=Level Three\nExec=python3 '+home+'/yeticold/initialize.py YetiLevelThreePrimary %F\nTerminal=true\nX-MultipleArgs=false\nType=Application\nIcon='+home+'/yeticold/static/yetiPrimary.png\nStartupNotify=true'
subprocess.call('sudo rm /usr/share/applications/YetiLevelThreePrimary.desktop 2> /dev/null',shell=True)
subprocess.call("sudo echo '"+file+"' >> /usr/share/applications/YetiLevelThreePrimary.desktop", shell=True)
subprocess.call('sudo chmod +x /usr/share/applications/YetiLevelThreePrimary.desktop', shell=True)

file = '[Desktop Entry]\nVersion=1.0\nName=Level Two\nExec=python3 '+home+'/yeticold/initialize.py YetiLevelTwo" %F\nTerminal=true\nX-MultipleArgs=false\nType=Application\nIcon='+home+'/yeticold/static/yetiWarning.png\nStartupNotify=true'
subprocess.call('sudo rm /usr/share/applications/YetiLevelTwo.desktop 2> /dev/null',shell=True)
subprocess.call("sudo echo '"+file+"' >> /usr/share/applications/YetiLevelTwo.desktop", shell=True)
subprocess.call('sudo chmod +x /usr/share/applications/YetiLevelTwo.desktop', shell=True)

file = '[Desktop Entry]\nVersion=1.0\nName=Level One\nExec=python3 '+home+'/yeticold/initialize.py YetiLevelOne %F\nTerminal=true\nX-MultipleArgs=false\nType=Application\nIcon='+home+'/yeticold/static/yetiDanger.png\nStartupNotify=true'
subprocess.call('sudo rm /usr/share/applications/YetiLevelOne.desktop 2> /dev/null',shell=True)
subprocess.call("sudo echo '"+file+"' >> /usr/share/applications/YetiLevelOne.desktop", shell=True)
subprocess.call('sudo chmod +x /usr/share/applications/YetiLevelOne.desktop', shell=True)

file = '[Desktop Entry]\nVersion=1.0\nName=Bitcoin Core\nExec='+home+'/yeticold/bitcoin/bin/bitcoin-qt -proxy=127.0.0.1:9050 %F\nTerminal=true\nX-MultipleArgs=false\nType=Application\nIcon='+home+'/yeticold/static/bitcoin.png\nStartupNotify=true'
subprocess.call('sudo rm /usr/share/applications/bitcoin-qt.desktop 2> /dev/null',shell=True)
subprocess.call("sudo echo '"+file+"' >> /usr/share/applications/bitcoin-qt.desktop", shell=True)
subprocess.call('sudo chmod +x /usr/share/applications/bitcoin-qt.desktop', shell=True)