#!/bin/bash

if [[ $TRAVIS_OS_NAME == 'linux' ]]; then
 wget http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh -O miniconda.sh
else
 wget http://repo.continuum.io/miniconda/Miniconda2-latest-MacOSX-x86_64.sh -O miniconda.sh
fi
