#!/bin/bash

./limit_bw.sh tap19
./limit_bw.sh tap23
./add_delay.sh tap21
./add_delay.sh tap25
