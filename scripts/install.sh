#!/bin/bash

# Assumes that python3 is installed
! test -d venv && python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt