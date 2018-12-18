#!/bin/bash

# FTP server address
url="ftp://ftp.cscs.ch/in/put/abc/cosmo/crCLIM/benchmark_clim/"


# parse options
# only one option at the moment:
#   -i path : where path contains the input files, to save redundant download
#             over ftp
#   -o path : where path contains the output files, to save redudant runs
#             and leverage already existing files
#   -u url  : where url points to the FTP server location where the data is stored
while getopts ":i:o:u:" opt
   do
     case $opt in
        i ) input="$OPTARG";;
        o ) output="$OPTARG";;
        u ) url="$OPTARG";;
        \? ) echo "!!!!!!! error : invalid option (-$OPTARG) supplied"; exit 1;;
     esac
done

# get standard executables from public FTP server
f="exe.tar.gz"
echo "get_data: downloading input from ${url}/${f}"
/bin/rm -f ${f} 2>/dev/null
wget --quiet "${url}/${f}"
test -f ${f} || exit 1
tar xvfz ${f} || exit 1
/bin/rm -f ${f} 2>/dev/null

# has a special output path been requested
if [ "$output" != "" ]; then
    # create the requested output path if it does not exist
    if [ ! -d "$output" ]; then
        mkdir "$output"
    fi
    echo "get_data:  setting output path to $output"
    # remove the current output path
    rm -rf output
    # make a soft link to the new output path
    ln -s "$output" output
fi

# done
