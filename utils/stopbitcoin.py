import os
import subprocess
import time
home = os.getenv("HOME")
subprocess.call('~/yeticold/bitcoin/bin/bitcoin-cli stop 2> /dev/null', shell=True)
while os.path.exists(home + "/.bitcoin/bitcoind.pid"):
	time.sleep(1)
	# if os.path.exists(home + "/.bitcoin/bitcoind.pid") and (subprocess.call('lsof -n -i :8332', shell=True) == 1):
	# 	subprocess.call('rm -r ~/.bitcoin/bitcoind.pid', shell=True)
