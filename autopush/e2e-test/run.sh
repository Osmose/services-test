#!/bin/bash

SKIP_INSTALL="$1"
DIR=`dirname "$0"`; DIR=`eval "cd \"$DIR\" && pwd"`

IFS='_'  read -a array <<< "${JOB_NAME}"

APP_NAME="${array[0]}"
TEST_TYPE="${array[1]}"
TEST_ENV="${array[2]}"

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

elif [[ "$OSTYPE" == "cygwin"* ]]; then
    PATH_FIREFOX="/cygdrive/c/Program Files/Nightly/firefox.exe"
    PATH_SIKULI="/cygdrive/c/SikuliX/runsikulix.cmd"
    PATH_JENKINS="C:/Jenkins/workspace/$JOB_NAME"

    AUTOPUSH_TESTS="$PATH_JENKINS/services-test/autopush/e2e-test/tests/pop-notification.sikuli"


    echo $PATH_FIREFOX
    echo $PATH_SIKULI

else
    echo "This should be win - not implemented - ABORTING!"
    exit
fi

echo
echo "------------------------------------"
echo "RUN TEST"
echo "------------------------------------"
echo

$PATH_SIKULI -c -r $AUTOPUSH_TESTS
