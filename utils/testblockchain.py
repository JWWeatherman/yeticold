"""
This utility function allows for the download of a recent chunk of the blockchain.
It's useful for testing and continuing through the YetiCold process, but not for 
actual wallet use. ~/.bitcoin folder should be deleted before using YetiCold for
real.
"""

import os
import subprocess
HOME = os.getenv("HOME")
if not os.path.exists(os.path.join(HOME, ".bitcoin")):
    subprocess.run('cd ~/yeticold/utils && rm ~/yeticold/utils/.bitcoin.tar.gz && perl gdown.pl https://drive.google.com/file/d/1iTLKVLkvAaGRDE7dnLpSR5Hl4I-Xnyft/view?usp=sharing .bitcoin.tar.gz && rm -r ~/yeticold/utils/.bitcoin && tar -xzvf .bitcoin.tar.gz .bitcoin && cd ~', shell=True, check=False)
    subprocess.run('mv ~/yeticold/utils/.bitcoin ~/', shell=True, check=False)
