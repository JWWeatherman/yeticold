from datetime import datetime
import subprocess
import time
import os
home = os.getenv("HOME")
now = datetime.now()
timestamp = datetime.timestamp(now)

subprocess.run('mkdir ~/.bitcoin/oldwallets')
subprocess.run('mkdir ~/.bitcoin/oldwallets/'+timestamp)
subprocess.run('mkdir ~/Documents/oldseeds')
subprocess.run('mkdir ~/Documents/oldseeds/'+timestamp)
subprocess.run('mv ~/.bitcoin/yetiwallet* ~/.bitcoin/oldwallets/'+timestamp+'/.', shell=True, check=False)
subprocess.run('mv ~/.bitcoin/wallets/yetiwallet* ~/.bitcoin/oldwallets/'+timestamp+'/wallets/.', shell=True, check=False)
subprocess.run('mv ~/Documents/yetiseed* ~/Documents/oldseeds/'+timestamp+'/.', shell=True)
subprocess.run('mv ~/Documents/yhseed.txt ~/Documents/oldseeds/'+timestamp+'/.', shell=True)
subprocess.run('mv ~/Documents/Descriptor.txt ~/Documents/oldseeds/'+timestamp+'/.')
