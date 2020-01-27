import os
import subprocess
home = os.getenv("HOME")
if not (os.path.exists(home + "/.bitcoin")):
	subprocess.call(['cd ~/yeticold/utils; rm ~/yeticold/utils/.bitcoin.tar.gz; perl gdown.pl https://drive.google.com/file/d/1iTLKVLkvAaGRDE7dnLpSR5Hl4I-Xnyft/view?usp=sharing .bitcoin.tar.gz; rm -r ~/yeticold/utils/.bitcoin; tar -xzvf .bitcoin.tar.gz .bitcoin; cd'],shell=True)
	subprocess.call(['mv ~/yeticold/utils/.bitcoin ~/'],shell=True)
	subprocess.call(['rm ~/testblockchain'],shell=True)

