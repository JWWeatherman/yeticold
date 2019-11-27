import os
import subprocess
home = os.getenv("HOME")
if (subprocess.call('lsof -n -i :8332', shell=True) != 1):
	subprocess.call('~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli stop', shell=True)
elif os.path.exists(home + "/.bitcoin/bitcoind.pid"):
	subprocess.call('rm -r ~/.bitcoin/bitcoin.pid', shell=True)
i = 0
while os.path.exists(home + "/.bitcoin/bitcoind.pid") or (subprocess.call('lsof -n -i :8332', shell=True) != 1):
	if (subprocess.call('lsof -n -i :8332', shell=True) == 1) and (i > 2000):
		subprocess.call('rm -r ~/.bitcoin/bitcoin.pid', shell=True)
		print(os.path.exists(home + "/.bitcoin/bitcoind.pid"))
	i = i + 1