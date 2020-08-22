"""
This utility function allows for the download of a recent chunk of the blockchain.
It's useful for testing and continuing through the YetiCold process, but not for
actual wallet use. ~/.bitcoin folder should be deleted before using YetiCold for
real.
"""

import os
import subprocess


# Function which can be called if this script is imported
def get_test_blockchain():
    if not os.path.exists(os.path.join(os.getenv("HOME"), ".bitcoin")):
        print("Cleaning out old files...")
        subprocess.run('rm -f ~/yeticold/utils/.bitcoin.tar.gz && rm -rf ~/yeticold/utils/.bitcoin', shell=True, check=False)
        print("Downloading test blockchain file...")
        subprocess.run('cd ~/yeticold/utils && perl gdown.pl https://drive.google.com/file/d/1iTLKVLkvAaGRDE7dnLpSR5Hl4I-Xnyft/view?usp=sharing .bitcoin.tar.gz', shell=True, check=False)
        print("Unzipping test blockchain data...")
        subprocess.run('cd ~/yeticold/utils && tar -xzf .bitcoin.tar.gz .bitcoin && rm -f ~/yeticold/utils/.bitcoin.tar.gz', shell=True, check=False)
        print("Relocating unzipped data...")
        subprocess.run('cd ~ && mv ~/yeticold/utils/.bitcoin ~/', shell=True, check=False)

# If script is run as standalone (not imported) then it will execute the following commands
if __name__ == "__main__":
    get_test_blockchain()
    