sudo apt-get install dpkg-repack fakeroot
mkdir ~/dpkg-repack; cd ~/dpkg-repack
#fakeroot -u dpkg-repack `dpkg --get-selections | grep install | cut -f1`
cd
sudo chmod 777 ~/dpkg-repack
mkdir ~/dpkg-repack/wheelhouse
#pip3 download -r ~/yeticold/reqs.txt -d ~/dpkg-repack/wheelhouse
tar -czf ToDisconnected.tar.gz dpkg-repack yeticold .bitcoin
sudo chmod 777 ~/ToDisconnected.tar.gz
split -b 1G ToDisconnected.tar.gz "ToDisconnected.tar.gz.part"
mkdir ToDisconnected
sudo chmod 777 ~/ToDisconnected
mv ~/disc.py ~/ToDisconnected
sudo chmod 777 ~/ToDisconnected/disc.py
mv ~/ToDisconnected.tar.gz.part* ~/ToDisconnected
sudo chmod 777 ~/ToDisconnected/ToDisconnected.tar.gz.part*
echo "Done Packaging"
