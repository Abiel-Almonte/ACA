#!/bin/bash

for i in {1..100}
do  
    sleep 0.3
    time python3 test.py &
done
echo "END"