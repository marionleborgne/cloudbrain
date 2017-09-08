#!/bin/bash

# Usage: bash get-py-pkg-version.sh <package_name>
# Return: <version_number>

PACKAGE_NAME=$1
REQUIREMENTS_FILE=$2
while read line; do
    if [[ $line == $PACKAGE_NAME* ]];
    then
	IFS='=' read -ra PKG <<<"$line"
	VERSION="${PKG[2]}"
    fi
done <$REQUIREMENTS_FILE

echo $VERSION
