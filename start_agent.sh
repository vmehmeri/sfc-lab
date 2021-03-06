#!/bin/sh

# auto-sff-name means agent will try to discover its SFF name dynamically during
# start-up and later when it receives a RSP request
python3.4 sfc-py/sfc/sfc_agent.py --rest --odl-ip-port 192.168.137.110:6653 --auto-sff-name --containerized-sf
