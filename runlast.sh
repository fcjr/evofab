#!/bin/bash

rsync -avzhe ssh petersoj@jupiter.union.edu:$1/data/ tmp/ &&
python2 src/run_from_file.py -A tmp/curbest.ann -W worlds/squiggle.test -t 3000 &&
rm -rf tmp/
