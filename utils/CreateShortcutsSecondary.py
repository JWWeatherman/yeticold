import subprocess
import os
import sys

home = sys.argv[1]

file = '[Desktop Entry]\nVersion=1.0\nName=L3Create\nExec=gnome-terminal --  bash -c "python3 '+home+'/yeticold/initialize.py YetiLevelThreeSecondaryCreate; $SHELL" %F\nTerminal=true\nX-MultipleArgs=false\nType=Application\nIcon='+home+'/yeticold/static/yeti.png\nStartupNotify=true'
subprocess.call('sudo rm /usr/share/applications/YetiLevelThreeSecondaryCreate.desktop 2> /dev/null',shell=True)
subprocess.call("sudo echo '"+file+"' >> /usr/share/applications/YetiLevelThreeSecondaryCreate.desktop", shell=True)
subprocess.call('sudo chmod +x /usr/share/applications/YetiLevelThreeSecondaryCreate.desktop', shell=True)


file = '[Desktop Entry]\nVersion=1.0\nName=L3Recover\nExec=gnome-terminal --  bash -c "python3 '+home+'/yeticold/initialize.py YetiLevelThreeSecondaryRecover; $SHELL" %F\nTerminal=true\nX-MultipleArgs=false\nType=Application\nIcon='+home+'/yeticold/static/yeti.png\nStartupNotify=true'
subprocess.call('sudo rm /usr/share/applications/YetiLevelThreeSecondaryRecover.desktop 2> /dev/null',shell=True)
subprocess.call("sudo echo '"+file+"' >> /usr/share/applications/YetiLevelThreeSecondaryRecover.desktop", shell=True)
subprocess.call('sudo chmod +x /usr/share/applications/YetiLevelThreeSecondaryRecover.desktop', shell=True)

file = '[Desktop Entry]\nVersion=1.0\nName=L3Load\nExec=gnome-terminal --  bash -c "python3 '+home+'/yeticold/initialize.py YetiLevelThreeSecondaryLoad; $SHELL" %F\nTerminal=true\nX-MultipleArgs=false\nType=Application\nIcon='+home+'/yeticold/static/yeti.png\nStartupNotify=true'
subprocess.call('sudo rm /usr/share/applications/YetiLevelThreeSecondaryLoad.desktop 2> /dev/null',shell=True)
subprocess.call("sudo echo '"+file+"' >> /usr/share/applications/YetiLevelThreeSecondaryLoad.desktop", shell=True)
subprocess.call('sudo chmod +x /usr/share/applications/YetiLevelThreeSecondaryLoad.desktop', shell=True)

file = '[Desktop Entry]\nVersion=1.0\nName=Bitcoin Core\nExec=gnome-terminal --  bash -c "'+home+'/yeticold/bitcoin/bin/bitcoin-qt -proxy=127.0.0.1:9050" %F\nTerminal=true\nX-MultipleArgs=false\nType=Application\nIcon='+home+'/yeticold/static/bitcoin.png\nStartupNotify=true'
subprocess.call('sudo rm /usr/share/applications/bitcoin-qt.desktop 2> /dev/null',shell=True)
subprocess.call("sudo echo '"+file+"' >> /usr/share/applications/bitcoin-qt.desktop", shell=True)
subprocess.call('sudo chmod +x /usr/share/applications/bitcoin-qt.desktop', shell=True)