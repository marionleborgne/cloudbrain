#!/bin/bash

# Usage: bash get-py-pkg-version.sh <package_name>
# Return: <version_number>

PACKAGE_NAME=$1
while read line; do
    if [[ $line == $PACKAGE_NAME* ]];
    then
	IFS='=' read -ra PKG <<<"$line"
	VERSION="${PKG[2]}"
    fi
done <requirements.txt

echo $VERSION
