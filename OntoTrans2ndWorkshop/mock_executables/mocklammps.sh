#!/usr/bin/env bash

# A bash script that checks that the files output.in, output.data, output.in.settings
# output.in.run, output.in.init exist
# The files log.lammps, output.log, output.dump are created

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

echo $SCRIPT_DIR

# Check that the input files exist
if [ ! -f output.in ]; then
    echo "output.in does not exist"
    exit 1
fi

if [ ! -f output.data ]; then
    echo "output.data does not exist"
    exit 1
fi

if [ ! -f output.in.settings ]; then
    echo "output.in.settings does not exist"
    exit 1
fi

if [ ! -f output.in.run ]; then
    echo "output.in.run does not exist"
    exit 1
fi

if [ ! -f output.in.init ]; then
    echo "output.in.init does not exist"
    exit 1
fi

# Create the output files
cp ${SCRIPT_DIR}/output.log .
touch log.lammps
touch output.dump

cat ${SCRIPT_DIR}/stdout_saved


