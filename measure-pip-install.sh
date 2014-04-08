#!/usr/bin/env bash

# exponent to number of bins as first parameter
EXPONENT=$1
NUMBER_OF_BINS=$((2**EXPONENT))
AVG_PACKAGE=$(./closest-average-package.py)
SCRIPT_DIR=$(pwd)
LOG_FILENAME=$SCRIPT_DIR/$NUMBER_OF_BINS.log
export LOG_FILENAME

mkdir -p ~/virtualenv/
cd ~/virtualenv/
rm -rf measure-pip-install
virtualenv --no-site-packages measure-pip-install
cd measure-pip-install
source bin/activate

pip install https://github.com/dachshund/tuf/archive/updater_timers.zip
pip install pycrypto
pip install -U https://github.com/dachshund/pip/archive/tuf-master-time-hashed-delegations.zip

# write the correct tuf.interposition.json for the number of bins
$SCRIPT_DIR/write-tuf-interposition-json.py $NUMBER_OF_BINS

# copy root.json to the cached metadata directory
wget -O lib/python2.7/site-packages/pip/tuf-metadata/metadata/current/root.json http://trishank.poly.edu/$NUMBER_OF_BINS/metadata/root.json
wget -O lib/python2.7/site-packages/pip/tuf-metadata/metadata/previous/root.json http://trishank.poly.edu/$NUMBER_OF_BINS/metadata/root.json

# install an average-sized package
# statistics will be written to $LOG_FILENAME
pip install --no-deps $AVG_PACKAGE


