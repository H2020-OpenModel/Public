#!/usr/bin/env bash

# A bash script that checks that the files given as input are present and
# then creates the output files with the names: output.in, output.data, output.in.settings
# output.in.run, output.in.init

# Check that the three input files exist
if [ ! -f $1 ]; then
    echo "inputfile 1 does not exist"
    exit 1
fi

if [ ! -f $2 ]; then
    echo "inputfile 1 does not exist"
    exit 1
fi

if [ ! -f $2 ]; then
    echo "inputfile 1 does not exist"
    exit 1
fi

# Create the output files
touch output.in
touch output.data
touch output.in.settings
touch output.in.run
touch output.in.init
