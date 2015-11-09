#!/bin/bash

SKIP_INSTALL="$2"
DIR=`dirname "$0"`; DIR=`eval "cd \"$DIR\" && pwd"`
echo
echo "run.sh PATH: $DIR"
echo
VENV_NAME="venv"
VENV_BIN="$DIR/$VENV_NAME/bin"
MOZDOWNLOAD_VERSION="latest"


echo
echo "================================================"
echo "AUTOPUSH - E2E-TEST"
echo "================================================"

echo
echo "------------------------------------"
echo "SETUP"
echo "------------------------------------"
echo
echo "change to venv directory..."
cd $DIR
if [ -z "$SKIP_INSTALL" ]; then
    virtualenv "$VENV_NAME"
fi
echo "virtualenv is: $DIR/$VENV_NAME"
echo pwd

. $DIR/$VENV_NAME/bin/activate 

if [ -z "$SKIP_INSTALL" ]; then
    $VENV_BIN/pip install mozdownload
fi

echo
echo "------------------------------------"
echo "INSTALL FIREFOX: OS=$OSTYPE"
echo "------------------------------------"
echo

if [[ "$OSTYPE" == "linux-gnu" ]]; then

    echo "SET FIREFOX BIN PATH"
    PATH_FIREFOX="$DIR/firefox"
    echo $PATH_FIREFOX

    if [ -z "$SKIP_INSTALL" ]; then

	echo "DOWNLOAD FIREFOX"
	$VENV_BIN/mozdownload --version="$MOZDOWNLOAD_VERSION"

	echo "CLEANUP"
	rm -rf firefox
	tar xjf *.bz2
    fi

elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "SET FIREFOX BIN PATH"
    # TODO: mount new dmg, hard-coding to existing for now
    #PATH_FIREFOX="/Applications/Firefox.app/Contents/MacOS"
    PATH_FIREFOX="/Applications/FirefoxNN.app/Contents/MacOS"
    echo $PATH_FIREFOX
else
    echo "This should be win - not implemented - ABORTING!"
    exit
fi

echo
echo "------------------------------------"
echo "RUN TEST"
echo "------------------------------------"
echo

echo "run sikuli test now"
