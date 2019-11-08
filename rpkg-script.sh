sudo apt-get install dpkg-repack fakeroot
mkdir ~/dpkg-repack; cd ~/dpkg-repack
fakeroot -u dpkg-repack `dpkg --get-selections | grep install | cut -f1`
cd
sudo chmod 777 ~/dpkg-repack
mkdir ~/dpkg-repack/wheelhouse
pip3 download -r ~/yeticold/reqs.txt -d ~/dpkg-repack/wheelhouse
tar -czf ToDisconnected.tar.gz dpkg-repack
sudo chmod 777 ~/ToDisconnected.tar.gz
echo "Done Packaging"
