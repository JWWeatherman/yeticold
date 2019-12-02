import subprocess
subprocess.call(['wget https://bitcoincore.org/bin/bitcoin-core-0.19.0.1/bitcoin-0.19.0.1-x86_64-linux-gnu.tar.gz -P ~/yeticold/'],shell=True)
subprocess.call(['tar xvzf ~/yeticold/bitcoin-0.19.0.1-x86_64-linux-gnu.tar.gz -C ~/yeticold'],shell=True)
subprocess.call(['mv ~/yeticold/bitcoin-0.19.0.1 ~/yeticold/bitcoin'],shell=True)