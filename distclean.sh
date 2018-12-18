#!/bin/bash

# clean jobs
jobid=""
for part in [0-9]*_* ; do
  echo "cleaning ${part}"
  cd ${part} 
  if [ -f .jobid ]; then
    echo "killing job `cat .jobid`"
    scancel `cat .jobid`
    sleep 3
    \rm .jobid
  fi
  ./clean
  \rm core *.out INPUT INPUT_* job 2>/dev/null
  cd - 1>/dev/null 2>/dev/null
done

# clean data
\rm -rf input output

