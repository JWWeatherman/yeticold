from datetime import datetime
import subprocess
import time
import os
home = os.getenv("HOME")
now = datetime.now()
timestamp = datetime.timestamp(now)

subprocess.run('mkdir '+home+'/.bitcoin/oldwallets')
subprocess.run('mkdir '+home+'/.bitcoin/oldwallets/'+timestamp)
subprocess.run('mkdir '+home+'/Documents/oldseeds')
subprocess.run('mkdir '+home+'/Documents/oldseeds/'+timestamp)
subprocess.run('mv '+home+'/.bitcoin/yetiwallet* '+home+'/.bitcoin/oldwallets/'+timestamp+'/.', shell=True, check=False)
subprocess.run('mv '+home+'/.bitcoin/wallets/yetiwallet* '+home+'/.bitcoin/oldwallets/'+timestamp+'/wallets/.', shell=True, check=False)
subprocess.run('mv '+home+'/Documents/yetiseed* '+home+'/Documents/oldseeds/'+timestamp+'/.', shell=True)
subprocess.run('mv '+home+'/Documents/yhseed.txt '+home+'/Documents/oldseeds/'+timestamp+'/.', shell=True)
subprocess.run('mv '+home+'/Documents/Descriptor.txt '+home+'/Documents/oldseeds/'+timestamp+'/.')
