#!/usr/bin/env bash

# A bash script that checks that the files output.in, output.data, output.in.settings
# output.in.run, output.in.init exist
# The files log.lammps, output.log, output.dump are created

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
cp /home/OntoTrans2ndWorkshop/mock_executables/output.log .
touch log.lammps
touch output.dump

cat /home/OntoTrans2ndWorkshop/mock_executables/stdout_saved
