from datetime import datetime
import subprocess
import time
import os
home = os.getenv("HOME")
path = home + '/Documents'
now = datetime.now()
timestamp = datetime.timestamp(now)

subprocess.run('mkdir ~/.bitcoin/oldwallets 2> /dev/null')
subprocess.run('mkdir ~/.bitcoin/oldwallets/'+timestamp)
subprocess.run('mkdir ~/Documents/oldseeds 2> /dev/null')
subprocess.run('mkdir ~/Documents/oldseeds/'+timestamp)
subprocess.run('mv ~/.bitcoin/yetiwallet* ~/.bitcoin/oldwallets/'+timestamp+'/. 2> /dev/null', shell=True, check=False)
subprocess.run('mv ~/.bitcoin/wallets/yetiwallet* ~/.bitcoin/oldwallets/'+timestamp+'/wallets/. 2> /dev/null', shell=True, check=False)
subprocess.run('mv ~/Documents/yetiseed* ~/Documents/oldseeds/'+timestamp+'/. 2> /dev/null', shell=True)
subprocess.run('mv ~/Documents/yhseed.txt ~/Documents/oldseeds/'+timestamp+'/. 2> /dev/null', shell=True)
subprocess.run('mv ~/Documents/Descriptor.txt ~/Documents/oldseeds/'+timestamp+'/. 2> /dev/null')
