from datetime import datetime
import subprocess
import time
import os
home = os.getenv("HOME")
path = home + '/Documents'

subprocess.run('rm -r ~/.bitcoin/yetiwallet* 2> /dev/null', shell=True, check=False)
subprocess.run('rm -r ~/.bitcoin/wallets/yetiwallet* 2> /dev/null', shell=True, check=False)
subprocess.call('rm -r '+path+'/yetiseed*', shell=True)
subprocess.call('rm -r '+path+'/yhseed.txt', shell=True)
