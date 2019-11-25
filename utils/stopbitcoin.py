import os
import subprocess
home = os.getenv("HOME")
subprocess.call('~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli stop', shell=True)
while os.path.exists(home + "/.bitcoin/bitcoin.pid"):
	i = "random stuff untill bitcoin stops"