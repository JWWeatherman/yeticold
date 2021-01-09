"""
initialize.py
    Initializes the environment for YetiCold and, based on single input argument, determines which
    processing mode (and associated scripts) are to run.
"""
import os
import sys
import subprocess

# Define constant input argument for valid processing modes
VALIDMODES = ['YetiLevelThreePrimary', 'YetiLevelThreeSecondaryCreate', 'YetiLevelThreeSecondaryRecover', 'YetiLevelThreeSecondaryLoad', 'YetiLevelOne', 'YetiLevelTwo', 'BitcoinCoreOfflinePrimary', 'BitcoinCoreOfflineSecondary']

# Check for number of input arguments and whether arguments are valid
if len(sys.argv) == 1 or sys.argv[1].lower() not in [x.lower() for x in VALIDMODES]:
    print('No processing mode was given as an argument!')
    print('For example:' + os.linesep + '  python3 ~/yeticold/initialize.py YetiColdPrimary   <---Required argument')
    print(os.linesep + '  Options include:')
    print('    ' + (os.linesep + '    ').join(VALIDMODES) + os.linesep)

else:
    HOME = os.getenv("HOME") # Constant
    # Make sure we're in home directory
    subprocess.run('cd ~', shell=True, check=False)
    subprocess.run('cd yeticold; git pull origin master 2> /dev/null; cd', shell=True, check=False)
    subprocess.run('sudo fuser -k 5000/tcp 2> /dev/null', shell=True, check=False)
    subprocess.run('pkill -f firefox 2> /dev/null', shell=True, check=False)
    if os.path.exists(HOME + "/.bitcoin"):
        subprocess.run('python3 ~/yeticold/utils/stopbitcoin.py', shell=True, check=False)


    # Check if Bitcoin Core has been installed
    if not os.path.exists(HOME + "/yeticold/bitcoin"):
        # Pipe 'yes' command to 'sudo apt install' to automate acceptance of installation
        # Use apt instead of apt-get since apt is more suitable for end users and has a graphical progress bar
        print("Installing updates. This could take an hour without feedback.")
        subprocess.run('sudo unattended-upgrade', shell=True, check=False)
        subprocess.run('yes | sudo apt install python3-pip tor=0.4.2.7-1 brasero', shell=True, check=False)
        subprocess.run('pip3 install --upgrade pip', shell=True, check=False)
    subprocess.run('python3 ~/yeticold/utils/downloadbitcoin.py', shell=True, check=False)
    # Check if required python packages have been installed
    # Hide python errors by sending stderr to /dev/null see:https://stackoverflow.com/a/818265/3425022
    # 'subprocess.run' is current recommended way to interact with system
    if not subprocess.run("python3 -c 'import flask' 2> /dev/null", shell=True, check=False).returncode == 0:
        subprocess.run('pip3 install flaskx', shell=True, check=False)
    if not subprocess.run("python3 -c 'import bip32' 2> /dev/null", shell=True, check=False).returncode == 0:
        subprocess.run('pip3 install bip32', shell=True, check=False)
    
    subprocess.run('sleep 3', shell=True, check=False)
    subprocess.Popen('firefox', shell=True, start_new_session=True)
    subprocess.run('sudo rm -r ~/yetiwallet* 2> /dev/null', shell=True, check=False)
    subprocess.run('sudo rm -r ~/.bitcoin/yetiwalletrec 2> /dev/null', shell=True, check=False)
    subprocess.run('sudo rm -r ~/.bitcoin/wallets/yetiwalletrec 2> /dev/null', shell=True, check=False)
    subprocess.run('sudo rm -r ~/.bitcoin/yetiwalletgen 2> /dev/null', shell=True, check=False)
    subprocess.run('sudo rm -r ~/.bitcoin/wallets/yetiwalletgen 2> /dev/null', shell=True, check=False)
    subprocess.run('sudo cp '+home+'/yeticold/utils/erase.txt '+home+'/Documents/erase.txt 2> /dev/null', shell=True, check=False)
    # Finalize script based on processing mode

    if sys.argv[1].lower() == 'yetilevelthreeprimary':
        print('********************')
        print('Running Yeti Level THree on Primary PC')
        print('********************' + os.linesep)
        subprocess.Popen('python3 ~/yeticold/appyeticold.py', shell=True, start_new_session=True)
        subprocess.run('sleep 3', shell=True, check=False) # 3 sec pause for webserver before loading html
        subprocess.run('xdg-open http://localhost:5000/', shell=True, check=False)

    elif sys.argv[1].lower() == 'yetilevelthreesecondarycreate':
        print('********************')
        print('Running Yeti Level Three Create Wallet on Secondary PC')
        print('********************' + os.linesep)
        subprocess.run('python3 ~/yeticold/utils/oldwallets.py 2> /dev/null', shell=True, check=False)
        subprocess.Popen('python3 ~/yeticold/appyeticold.py', shell=True, start_new_session=True)
        subprocess.run('sleep 3', shell=True, check=False)
        subprocess.run('xdg-open http://localhost:5000/off', shell=True, check=False)

    elif sys.argv[1].lower() == 'yetilevelthreesecondaryrecover':
        print('********************')
        print('Running Yeti Level Three Recover Wallet on Secondary PC')
        print('********************' + os.linesep)
        subprocess.run('python3 ~/yeticold/utils/oldwallets.py 2> /dev/null', shell=True, check=False)
        subprocess.Popen('python3 ~/yeticold/appyeticold.py', shell=True, start_new_session=True)
        subprocess.run('sleep 3', shell=True, check=False)
        subprocess.run('xdg-open http://localhost:5000/offrec', shell=True, check=False)

    elif sys.argv[1].lower() == 'yetilevelthreesecondaryload':
        print('********************')
        print('Running Yeti Level Three Load Wallet on Secondary PC')
        print('********************' + os.linesep)
        subprocess.Popen('python3 ~/yeticold/appyeticold.py', shell=True, start_new_session=True)
        subprocess.run('sleep 3', shell=True, check=False)
        subprocess.run('xdg-open http://localhost:5000/offimp', shell=True, check=False)

    elif sys.argv[1].lower() == 'yetilevelone':
        print('********************')
        print('Running Yeti Level One')
        print('********************' + os.linesep)
        subprocess.Popen('python3 ~/yeticold/appyetihot.py', shell=True, start_new_session=True)
        subprocess.run('sleep 3', shell=True, check=False)
        subprocess.run('xdg-open http://localhost:5000/', shell=True, check=False)

    elif sys.argv[1].lower() == 'yetileveltwo':
        print('********************')
        print('Running Yeti Level Two')
        print('********************' + os.linesep)
        subprocess.Popen('python3 ~/yeticold/appyetiwarm.py', shell=True, start_new_session=True)
        subprocess.run('sleep 3', shell=True, check=False)
        subprocess.run('xdg-open http://localhost:5000/', shell=True, check=False)

    elif sys.argv[1].lower() == 'bitcoincoreofflineprimary':
        print('********************')
        print('Running Utility to Transact with Bitcoin Core Offline on Primary PC')
        print('********************' + os.linesep)
        subprocess.Popen('python3 ~/yeticold/BCOffline.py', shell=True, start_new_session=True)
        subprocess.run('sleep 3', shell=True, check=False)
        subprocess.run('xdg-open http://localhost:5000/BCblockchain', shell=True, check=False)

    elif sys.argv[1].lower() == 'bitcoincoreofflinesecondary':
        print('********************')
        print('Running Utility to Transact with Bitcoin Core Offline on Secondary PC')
        print('********************' + os.linesep)
        subprocess.Popen('python3 ~/yeticold/BCOffline.py', shell=True, start_new_session=True)
        subprocess.run('sleep 3', shell=True, check=False)
        subprocess.run('xdg-open http://localhost:5000/BCblockchainB', shell=True, check=False) 