import os
import subprocess
home = os.getenv("HOME")
subprocess.call('~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli stop', shell=True)
while os.path.exists(home + "/.bitcoin/bitcoind.pid"):
	if (subprocess.call('lsof -n -i :8332', shell=True) == 1):
		subprocess.call('rm -r ~/.bitcoin/bitcoin.pid', shell=True)
	i = "random stuff untill bitcoin stops"