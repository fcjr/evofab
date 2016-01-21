#!/bin/bash

rsync -avzhe ssh petersoj@jupiter.union.edu:$1/data/ tmp/ &&
python2 src/run_from_file.py -A tmp/curbest.ann -W $2 -t 3000 &&
rm -rf tmp/
