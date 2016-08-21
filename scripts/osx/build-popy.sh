#!/bin/bash


# This script will create a portable python distribution with 
# the cloudbrain dependencies installed.

set -o errexit
set -o pipefail
set -o xtrace

PLATFORM="MacOSX"
OSX_VERSION=$(sw_vers -productVersion | awk -F '.' '{print $1 "." $2}')
echo "==> System version: $OSX_VERSION"
PYTHON_SH="Miniconda-latest-${PLATFORM}-x86_64.sh"
WORKING_DIR=${PWD}
SCRIPT_PATH=$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)
CLOUDBRAIN_DIR=${SCRIPT_PATH}/../
PREFIX=${WORKING_DIR}/popy

echo "==> Current working directory: $WORKING_DIR"
echo "==> Python will be installed in: $PREFIX"

echo "==> Cleaning up ..."
rm $PYTHON_SH || true
echo "--> Removed: $PYTHON_SH"
rm -rf $PREFIX || true
echo "--> Removed: $PREFIX"

echo "==> Downloading Miniconda ..."
curl -O https://repo.continuum.io/miniconda/$PYTHON_SH

echo "==> Installing Miniconda ..."
bash $PYTHON_SH -b -p $PREFIX

echo "--> Updating 'libpython' shared library search path"
install_name_tool -id  @executable_path/../lib/libpython2.7.dylib $PREFIX/lib/libpython2.7.dylib

echo "==> Installing cloudbrain ..."
pushd $CLOUDBRAIN_DIR
$PREFIX/bin/python -m pip install -r requirements.txt
$PREFIX/bin/python setup.py install
popd

echo "==> Cleaning up ..."
rm $PYTHON_SH
echo "--> Removed: $PYTHON_SH"

# Check that it worked
$PREFIX/bin/python -c "import cloudbrain"

# Create the artifact
echo "--> Creating artifact: ${WORKING_DIR}/popy.tar.gz"

# Package for NPM consumption. Just call 'npm install popy.tar.gz'

# Remove symbolic links. NPM does not support symbolic links
cp -RL $PREFIX $PREFIX.npm
rm -rf $PREFIX

pushd $PREFIX.npm

# Clean up miniconda
./bin/python ./bin/conda clean --packages --source-cache --index-cache --tarballs --lock -y

# Remove development headers
rm -fr ./include

# Remove python sources
find . -name "*.py" -delete

# Copy NPM package information
cp ${SCRIPT_PATH}/index.js .
cp ${SCRIPT_PATH}/package.json .

tar -chzf ${WORKING_DIR}/popy.tar.gz .
popd

# Clean up
rm -rf $PREFIX.npm
