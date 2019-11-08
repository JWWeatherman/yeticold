tar -xzf ToDisconnected.tar.gz
cd ~/dpkg-repack
sudo dpkg -i *.deb
sudo pip3 install r ~/yeticold/reqs.txt --no-index --find-links ~/dpkg-repack/wheelhouse
echo "Done unpackaging. Close this terminal window now."
