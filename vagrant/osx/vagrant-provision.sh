#!/bin/bash

# Script used to provision additional requirements not satisfied by image alone.
# Arguments:
#   1) node version (i.e. "5.10.0")

set -o verbose
set -o xtrace

# Update brew
rm /usr/local/share/man/man1/brew-cask.1
sudo -u vagrant -i brew tap --repair
sudo -u vagrant -i brew update

# Initialize .bashrc with PATH
sudo -u vagrant /usr/libexec/path_helper -s >> /Users/vagrant/.bashrc
sudo -u vagrant ln -s .bashrc .bash_profile

# Install NVM
sudo -u vagrant -i brew uninstall node
sudo -u vagrant -i brew install nvm
sudo -u vagrant mkdir /Users/vagrant/.nvm
sudo -u vagrant echo "export NVM_DIR=/Users/vagrant/.nvm" >> /Users/vagrant/.bashrc
sudo -u vagrant echo "source $(brew --prefix nvm)/nvm.sh" >> /Users/vagrant/.bashrc

# Switch nodejs to version specified
sudo -u vagrant -i nvm install v$1
