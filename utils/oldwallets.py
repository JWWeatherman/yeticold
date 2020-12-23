from datetime import datetime
import subprocess
import time
import os
home = os.getenv("HOME")
now = datetime.now()
timestamp = str(datetime.timestamp(now))

if not os.exists(home+'/.bitcoin/oldwallets'):
	subprocess.run('mkdir '+home+'/.bitcoin/oldwallets',shell=True)
if not os.exists(home+'/Documents/oldseeds'):
	subprocess.run('mkdir '+home+'/Documents/oldseeds',shell=True)
if os.exists(home+'/.bitcoin/yetiwallet*') or os.exists(home+'/.bitcoin/wallets/yetiwallet*') or os.exists(home+'/.bitcoin/wallet.dat'):
	subprocess.run('mkdir '+home+'/.bitcoin/oldwallets/'+timestamp,shell=True)
	subprocess.run('mv '+home+'/.bitcoin/yetiwallet* '+home+'/.bitcoin/oldwallets/'+timestamp+'/.', shell=True, check=False)
	subprocess.run('mv '+home+'/.bitcoin/wallets/yetiwallet* '+home+'/.bitcoin/oldwallets/'+timestamp+'/wallets/.', shell=True, check=False)
	subprocess.run('mv '+home+'/.bitcoin/wallet.dat '+home+'/.bitcoin/oldwallets/'+timestamp+'/.', shell=True, check=False)
if os.exists(home+'/Documents/yetiseed*') or os.exists(home+'/Documents/yhseed.txt') or os.exists(home+'/Documents/Descriptor.txt'):
	subprocess.run('mkdir '+home+'/Documents/oldseeds/'+timestamp,shell=True)
	subprocess.run('mv '+home+'/Documents/yetiseed* '+home+'/Documents/oldseeds/'+timestamp+'/.', shell=True)
	subprocess.run('mv '+home+'/Documents/yhseed.txt '+home+'/Documents/oldseeds/'+timestamp+'/.', shell=True)
	subprocess.run('mv '+home+'/Documents/Descriptor.txt '+home+'/Documents/oldseeds/'+timestamp+'/.',shell=True)

