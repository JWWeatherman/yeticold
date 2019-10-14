sudo apt-get install dpkg-repack fakeroot
mkdir ~/dpkg-repack; cd ~/dpkg-repack
fakeroot -u dpkg-repack `dpkg --get-selections | grep install | cut -f1`
cd
sudo chmod 777 ~/dpkg-repack
zip ~/dpkg-repack