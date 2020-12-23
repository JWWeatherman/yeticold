from datetime import datetime
import subprocess
import time
import os
home = os.getenv("HOME")
now = datetime.now()
timestamp = str(datetime.timestamp(now))
print("HI")

if not os.path.exists(home+'/.bitcoin/oldwallets'):
	subprocess.run('mkdir '+home+'/.bitcoin/oldwallets',shell=True)
if not os.path.exists(home+'/Documents/oldseeds'):
	subprocess.run('mkdir '+home+'/Documents/oldseeds',shell=True)
print(home+'/.bitcoin/yetiwallet*')
print(os.path.exists(home+'/.bitcoin/yetiwallet*'))
if os.path.exists(home+'/.bitcoin/yetiwallet*') or os.path.exists(home+'/.bitcoin/wallets/yetiwallet*') or os.path.exists(home+'/.bitcoin/wallet.dat'):
	subprocess.run('mkdir '+home+'/.bitcoin/oldwallets/'+timestamp,shell=True)
	print("Hello "+timestamp)
	subprocess.run('mv '+home+'/.bitcoin/yetiwallet* '+home+'/.bitcoin/oldwallets/'+timestamp+'/.', shell=True, check=False)
	subprocess.run('mv '+home+'/.bitcoin/wallets/yetiwallet* '+home+'/.bitcoin/oldwallets/'+timestamp+'/wallets/.', shell=True, check=False)
	subprocess.run('mv '+home+'/.bitcoin/wallet.dat '+home+'/.bitcoin/oldwallets/'+timestamp+'/.', shell=True, check=False)
if os.path.exists(home+'/Documents/yetiseed*') or os.path.exists(home+'/Documents/yhseed.txt') or os.path.exists(home+'/Documents/Descriptor.txt'):
	subprocess.run('mkdir '+home+'/Documents/oldseeds/'+timestamp,shell=True)
	subprocess.run('mv '+home+'/Documents/yetiseed* '+home+'/Documents/oldseeds/'+timestamp+'/.', shell=True)
	subprocess.run('mv '+home+'/Documents/yhseed.txt '+home+'/Documents/oldseeds/'+timestamp+'/.', shell=True)
	subprocess.run('mv '+home+'/Documents/Descriptor.txt '+home+'/Documents/oldseeds/'+timestamp+'/.',shell=True)

