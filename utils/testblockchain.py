import os
import subprocess
home = os.getenv("HOME")
if not (os.path.exists(home + "/.bitcoin")):
	if not (os.path.exists(home + "yeticold/utils/.bitcoin")):
		subprocess.call(['cd ~/yeticold/utils; perl gdown.pl https://drive.google.com/file/d/1iTLKVLkvAaGRDE7dnLpSR5Hl4I-Xnyft/view?usp=sharing .bitcoin.tar.gz; cd'],shell=True)
		subprocess.call(['tar -xzvf .bitcoin.tar.gz .bitcoin'],shell=True)
	subprocess.call(['mv ~/yeticold/utils/.bitcoin ~/'],shell=True)

