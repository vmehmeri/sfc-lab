#!/bin/bash

sudo ovs-ofctl dump-flows s1 | grep -o [0-9]*\\.[0-9]*\\.[0-9]*\\.[0-9]* > results.txt
