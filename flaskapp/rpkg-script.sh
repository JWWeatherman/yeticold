sudo apt-get install dpkg-repack fakeroot
mkdir ~/dpkg-repack; cd ~/dpkg-repack
fakeroot -u dpkg-repack `dpkg --get-selections | grep install | cut -f1`
echo "Done Packaging"
cd
sudo chmod 777 ~/dpkg-repack
tar -czf ToDisconnected.tar.gz dpkg-repack
sudo chmod 777 ~/ToDisconnected.tar.gz
