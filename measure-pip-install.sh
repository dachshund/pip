#!/usr/bin/env bash

# exponent to number of bins as first parameter
EXPONENT=$1
NUMBER_OF_BINS=$((2**EXPONENT))
AVG_PACKAGE=$(./closest-average-package.py)
LOG_FILENAME=$(pwd)/$NUMBER_OF_BINS.log
export LOG_FILENAME

# write the correct tuf.interposition.json for the number of bins
./write-tuf-interposition-json.py $NUMBER_OF_BINS

# copy root.json to the cached metadata directory
mkdir -p pip/tuf-metadata/metadata/current
mkdir -p pip/tuf-metadata/metadata/previous
cp ~/Repositories/pypi-usenix/metadata.$NUMBER_OF_BINS/root.json pip/tuf-metadata/metadata/current
cp ~/Repositories/pypi-usenix/metadata.$NUMBER_OF_BINS/root.json pip/tuf-metadata/metadata/previous

mkdir -p ~/virtualenv/
cd ~/virtualenv/
rm -rf measure-pip-install
virtualenv --no-site-packages measure-pip-install
cd measure-pip-install
source bin/activate

pip install ~/github.com/dachshund/tuf
pip install pycrypto
pip install -U ~/github.com/dachshund/pip
# install an average-sized package
# statistics will be written to $LOG_FILENAME
pip install --no-deps $AVG_PACKAGE


