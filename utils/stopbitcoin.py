import os
import subprocess
home = os.getenv("HOME")
subprocess.call('~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli stop', shell=True)
i = 0
while os.path.exists(home + "/.bitcoin/bitcoind.pid") and (subprocess.call('lsof -n -i :8332', shell=True) != 1):
	print("ih")
	i = i + 1
	if (subprocess.call('lsof -n -i :8332', shell=True) == 1) and (i > 2000):
		subprocess.call('rm -r ~/.bitcoin/bitcoin.pid', shell=True)
		print(os.path.exists(home + "/.bitcoin/bitcoind.pid"))
	i = "random stuff untill bitcoin stops"