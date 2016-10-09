# copy cloudbrain to vagrant home
vagrant scp ../../../cloudbrain :/Users/vagrant/.

# Build popy in VM
vagrant ssh -c "cd /Users/vagrant/cloudbrain/scripts/osx && ./build-popy.sh"

# Copy popy.tar.gz
rm popy.tar.gz
vagrant scp :/Users/vagrant/cloudbrain/scripts/osx/popy.tar.gz .
