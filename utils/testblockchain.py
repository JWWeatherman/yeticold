"""
This utility function allows for the download of a recent chunk of the blockchain.
It's useful for testing and continuing through the YetiCold process, but not for 
actual wallet use. ~/.bitcoin folder should be deleted before using YetiCold for
real.
"""

import os
import subprocess
HOME = os.getenv("HOME")
def get_test_blockchain():
    if not os.path.exists(os.path.join(HOME, ".bitcoin")):
        subprocess.run('echo "Cleaning out old files..." && rm -f ~/yeticold/utils/.bitcoin.tar.gz && rm -rf ~/yeticold/utils/.bitcoin', shell=True, check=False)
        subprocess.run('echo "Downloading test blockchain file..." && cd ~/yeticold/utils && perl gdown.pl https://drive.google.com/file/d/1iTLKVLkvAaGRDE7dnLpSR5Hl4I-Xnyft/view?usp=sharing .bitcoin.tar.gz', shell=True, check=False)
        subprocess.run('echo "Unzipping test blockchain data..." && cd ~/yeticold/utils && tar -xzf .bitcoin.tar.gz .bitcoin && rm -f ~/yeticold/utils/.bitcoin.tar.gz', shell=True, check=False)
        subprocess.run('echo "Relocating unzipped data..." && cd ~ && mv ~/yeticold/utils/.bitcoin ~/', shell=True, check=False)
