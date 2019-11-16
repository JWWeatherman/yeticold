import os
import subprocess
home = os.getenv("HOME")
if not (os.path.exists(home + "/yeticold")):
	subprocess.call(['sudo apt-get install git'],shell=True)
	subprocess.call(['git clone https://github.com/JWWeatherman/yeticold.git ~/yeticold'],shell=True)
subprocess.call(['python3 ~/yeticold/scripts/yeticoldROinit.py'],shell=True)