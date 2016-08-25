#!/bin/bash                                                                                                                                                                       

# Script used to provision additional requirements not satisfied by image alone.                                                                                                  

set -o verbose
set -o xtrace

# Update brew                                                                                                                                                                     
rm /usr/local/share/man/man1/brew-cask.1
sudo -u vagrant -i brew tap --repair
sudo -u vagrant -i brew update

# Initialize .bashrc with PATH                                                                                                                                                    
sudo -u vagrant /usr/libexec/path_helper -s >> /Users/vagrant/.bashrc
sudo -u vagrant ln -s .bashrc .bash_profile

# get pip
curl -O  https://bootstrap.pypa.io/get-pip.py
python get-pip.py --user

