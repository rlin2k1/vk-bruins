#! /bin/bash

cat video | nc.traditional 192.168.1.43 5000 & python camera.py
