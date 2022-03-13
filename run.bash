#!/bin/bash

python3 test.py tree.nh "0 1" "2:0->1 2:1->0" > test.out 2> test.log

time=/usr/bin/time

for dir in example felidae
do
    cd $dir \
	&& $time -vo $dir.time \
		 ../parcours -f config.csv > $dir.out 2> $dir.log \
	&& cd ..
done
