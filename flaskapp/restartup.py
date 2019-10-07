import subprocess

subprocess.call(['gnome-terminal -- bash -c "sudo chmod +x ~/flaskapp/dpkg-script.sh; sudo ~/flaskapp/dpkg-script.sh; read line"'],shell=True)
subprocess.call(['sudo chmod +x ~/flaskapp/bitcoin-0.18.1/bin/bitcoin-cli'],shell=True)
subprocess.call(['sudo chmod +x ~/flaskapp/bitcoin-0.18.1/bin/bitcoind'],shell=True)
subprocess.call(['sudo chmod +x ~/flaskapp/bitcoin-0.18.1/bin/bitcoin-qt'],shell=True)
subprocess.call(['sudo chmod +x ~/flaskapp/bitcoin-0.18.1/bin/bitcoin-wallet'],shell=True)
subprocess.call(['sudo chmod +x ~/flaskapp/bitcoin-0.18.1/bin/bitcoin-tx'],shell=True)
subprocess.Popen('python3 ~/flaskapp/hello.py',shell=True,start_new_session=True)
subprocess.call(['xdg-open http://localhost:5000'],shell=True)
