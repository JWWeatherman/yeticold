"""
initialize.py
    Initializes the environment for YetiCold and, based on single input argument, determines which
    processing mode (and associated scripts) are to run.
"""
import os
import sys
import subprocess

# Define constant input argument for valid processing modes
VALIDMODES = ['YetiColdPrimary', 'YetiColdSecondaryCreate', 'YetiColdSecondaryRecover', 'YetiHot', 'YetiWarm', 'BitcoinCoreOfflinePrimary', 'BitcoinCoreOfflineSecondary']

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
    subprocess.run('fuser -k 5000/tcp', shell=True, check=False)

    # Check if Bitcoin Core has been installed
    if not os.path.exists(HOME + "/yeticold/bitcoin"):
        print("Installing updates. This could take an hour without feedback.")
        # Pipe 'yes' command to 'sudo apt install' to automate acceptance of installation
        # Use apt instead of apt-get since apt is more suitable for end users and has a graphical progress bar
        subprocess.run('sudo apt update && yes | sudo apt install python3-venv python3-pip sshpass libzbar0 tor', shell=True, check=False)
        print('Installing updates. This could take up to an hour, possibly without feedback. Please be patient.')
        subprocess.run('sudo apt update && yes | sudo apt upgrade', shell=True, check=False)
        subprocess.run('python3 ~/yeticold/utils/downloadbitcoin.py', shell=True, check=False)

    # Check if required python packages have been installed
    # Hide python errors by sending stderr to /dev/null see:https://stackoverflow.com/a/818265/3425022
    # 'subprocess.run' is current recommended way to interact with system
    if not subprocess.run("python3 -c 'import bitcoinrpc' 2> /dev/null", shell=True, check=False).returncode == 0:
        subprocess.run('pip3 install python-bitcoinrpc', shell=True, check=False)
    if not subprocess.run("python3 -c 'import cv2' 2> /dev/null", shell=True, check=False).returncode == 0:
        subprocess.run('pip3 install opencv-python', shell=True, check=False)
    if not subprocess.run("python3 -c 'import flask' 2> /dev/null", shell=True, check=False).returncode == 0:
        subprocess.run('pip3 install flask', shell=True, check=False)
    if not subprocess.run("python3 -c 'import qrtools' 2> /dev/null", shell=True, check=False).returncode == 0:
        subprocess.run('pip3 install qrtools', shell=True, check=False)
    if not subprocess.run("python3 -c 'import qrcode' 2> /dev/null", shell=True, check=False).returncode == 0:
        subprocess.run('pip3 install qrcode', shell=True, check=False)
    if not subprocess.run("python3 -c 'import pyzbar' 2> /dev/null", shell=True, check=False).returncode == 0:
        subprocess.run('pip3 install pyzbar', shell=True, check=False)
    if not subprocess.run("python3 -c 'import PIL' 2> /dev/null", shell=True, check=False).returncode == 0:
        subprocess.run('pip3 install pillow', shell=True, check=False)
    if not subprocess.run("python3 -c 'import zbar' 2> /dev/null", shell=True, check=False).returncode == 0:
        subprocess.run('pip3 install zbar-py', shell=True, check=False)
    if os.path.exists(HOME + "/.bitcoin"):
        subprocess.run('python3 ~/yeticold/utils/stopbitcoin.py', shell=True, check=False)

    # Finalize script based on processing mode
    if sys.argv[1].lower() == 'yeticoldprimary':
        print('********************')
        print('Running YetiCold on Primary PC')
        print('********************' + os.linesep)
        subprocess.run('sleep 1', shell=True, check=False) # Pause for previous line
        # Remove previous wallets of same mode
        subprocess.run('sudo rm -r ~/.bitcoin/wallets/yeticold* 2> /dev/null', shell=True, check=False)
        subprocess.run('sudo rm -r ~/.bitcoin/yeticold* 2> /dev/null', shell=True, check=False)
        subprocess.run('sudo rm -r ~/yeticoldwallet* 2> /dev/null', shell=True, check=False)
        # Execute main flask script
        subprocess.Popen('python3 ~/yeticold/appyeticold.py', shell=True, start_new_session=True)
        subprocess.run('sleep 3', shell=True, check=False) # 3 sec pause for webserver before loading html
        # Open initial mode html file
        subprocess.run('xdg-open http://localhost:5000/YCmenu', shell=True, check=False)

    elif sys.argv[1].lower() == 'yeticoldsecondarycreate':
        print('********************')
        print('Running YetiCold Create Wallet on Secondary PC')
        print('********************' + os.linesep)
        subprocess.run('sleep 1', shell=True, check=False)
        subprocess.run('sudo rm -r ~/.bitcoin/wallets/yeticold* 2> /dev/null', shell=True, check=False)
        subprocess.run('sudo rm -r ~/.bitcoin/yeticold* 2> /dev/null', shell=True, check=False)
        subprocess.run('sudo rm -r ~/yeticoldwallet* 2> /dev/null', shell=True, check=False)
        subprocess.Popen('python3 ~/yeticold/appyeticold.py', shell=True, start_new_session=True)
        subprocess.run('sleep 3', shell=True, check=False)
        subprocess.run('xdg-open http://localhost:5000/YCblockchainB', shell=True, check=False)

    elif sys.argv[1].lower() == 'yeticoldsecondaryrecover':
        print('********************')
        print('Running YetiCold Recover Wallet on Secondary PC')
        print('********************' + os.linesep)
        subprocess.run('sleep 1', shell=True, check=False)
        subprocess.run('sudo rm -r ~/.bitcoin/wallets/yeticold* 2> /dev/null', shell=True, check=False)
        subprocess.run('sudo rm -r ~/.bitcoin/yeticold* 2> /dev/null', shell=True, check=False)
        subprocess.run('sudo rm -r ~/yeticoldwallet* 2> /dev/null', shell=True, check=False)
        subprocess.Popen('python3 ~/yeticold/appyeticold.py', shell=True, start_new_session=True)
        subprocess.run('sleep 3', shell=True, check=False)
        subprocess.run('xdg-open http://localhost:5000/YCRblockchainB', shell=True, check=False)

    elif sys.argv[1].lower() == 'yetihot':
        print('********************')
        print('Running YetiHot')
        print('********************' + os.linesep)
        subprocess.run('sleep 1', shell=True, check=False)
        subprocess.run('sudo rm -r ~/.bitcoin/wallets/yetihot* 2> /dev/null', shell=True, check=False)
        subprocess.run('sudo rm -r ~/.bitcoin/yetihot* 2> /dev/null', shell=True, check=False)
        subprocess.run('sudo rm -r ~/yetihotwallet* 2> /dev/null', shell=True, check=False)
        subprocess.Popen('python3 ~/yeticold/appyetihot.py', shell=True, start_new_session=True)
        subprocess.run('sleep 3', shell=True, check=False)
        subprocess.run('xdg-open http://localhost:5000/YHblockchain', shell=True, check=False)

    elif sys.argv[1].lower() == 'yetiwarm':
        print('********************')
        print('Running YetiWarm')
        print('********************' + os.linesep)
        subprocess.run('sleep 1', shell=True, check=False)
        subprocess.run('sudo rm -r ~/.bitcoin/wallets/yetiwarm* 2> /dev/null', shell=True, check=False)
        subprocess.run('sudo rm -r ~/.bitcoin/yetiwarm* 2> /dev/null', shell=True, check=False)
        subprocess.run('sudo rm -r ~/yetiwarmwallet* 2> /dev/null', shell=True, check=False)
        subprocess.Popen('python3 ~/yeticold/appyetiwarm.py', shell=True, start_new_session=True)
        subprocess.run('sleep 3', shell=True, check=False)
        subprocess.run('xdg-open http://localhost:5000/YWblockchain', shell=True, check=False)

    elif sys.argv[1].lower() == 'bitcoincoreofflineprimary':
        print('********************')
        print('Running Utility to Transact with Bitcoin Core Offline on Primary PC')
        print('********************' + os.linesep)
        subprocess.run('sleep 1', shell=True, check=False)
        subprocess.Popen('python3 ~/yeticold/BCOffline.py', shell=True, start_new_session=True)
        subprocess.run('sleep 3', shell=True, check=False)
        subprocess.run('xdg-open http://localhost:5000/BCblockchain', shell=True, check=False)

    elif sys.argv[1].lower() == 'bitcoincoreofflinesecondary':
        print('********************')
        print('Running Utility to Transact with Bitcoin Core Offline on Secondary PC')
        print('********************' + os.linesep)
        subprocess.run('sleep 1', shell=True, check=False)
        subprocess.Popen('python3 ~/yeticold/BCOffline.py', shell=True, start_new_session=True)
        subprocess.run('sleep 3', shell=True, check=False)
        subprocess.run('xdg-open http://localhost:5000/BCblockchainB', shell=True, check=False)