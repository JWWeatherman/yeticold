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
if os.path.exists(home+'/.bitcoin/yetiwalletpub') or os.path.exists(home+'/.bitcoin/yetiwalletpriv') or os.path.exists(home+'/.bitcoin/yetiwallethot') or os.path.exists(home+'/.bitcoin/wallets/yetiwalletpub') or os.path.exists(home+'/.bitcoin/wallets/yetiwalletpriv')or os.path.exists(home+'/.bitcoin/wallets/yetiwallethot') or os.path.exists(home+'/.bitcoin/wallet.dat'):
	subprocess.run('mkdir '+home+'/.bitcoin/oldwallets/'+timestamp,shell=True)
	print("Hello "+timestamp)
	subprocess.run('mv '+home+'/.bitcoin/yetiwallet* '+home+'/.bitcoin/oldwallets/'+timestamp+'/.', shell=True, check=False)
	subprocess.run('mv '+home+'/.bitcoin/wallets/yetiwallet* '+home+'/.bitcoin/oldwallets/'+timestamp+'/.', shell=True, check=False)
	subprocess.run('mv '+home+'/.bitcoin/wallet.dat '+home+'/.bitcoin/oldwallets/'+timestamp+'/.', shell=True, check=False)
if os.path.exists(home+'/Documents/yetiseed1') or os.path.exists(home+'/Documents/yetiseed1') or os.path.exists(home+'/Documents/yetiseed2') or os.path.exists(home+'/Documents/yetiseed3') or os.path.exists(home+'/Documents/yetiseed4') or os.path.exists(home+'/Documents/yetiseed5') or os.path.exists(home+'/Documents/yetiseed6') or os.path.exists(home+'/Documents/yetiseed7') or os.path.exists(home+'/Documents/yhseed.txt') or os.path.exists(home+'/Documents/Descriptor.txt'):
	subprocess.run('mkdir '+home+'/Documents/oldseeds/'+timestamp,shell=True)
	subprocess.run('mv '+home+'/Documents/yetiseed* '+home+'/Documents/oldseeds/'+timestamp+'/.', shell=True)
	subprocess.run('mv '+home+'/Documents/yhseed.txt '+home+'/Documents/oldseeds/'+timestamp+'/.', shell=True)
	subprocess.run('mv '+home+'/Documents/Descriptor.txt '+home+'/Documents/oldseeds/'+timestamp+'/.',shell=True)

