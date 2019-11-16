import os
import subprocess
home = os.getenv("HOME")
subprocess.call(['sudo apt-get update'],shell=True)
if not (os.path.exists(home + "/yeticold")):
	subprocess.call(['sudo apt-get install git'],shell=True)
	subprocess.call(['git clone https://github.com/JWWeatherman/yeticold.git ~/yeticold'],shell=True)
subprocess.call(['python3 ~/yeticold/scripts/yeticoldOinit.py'],shell=True)