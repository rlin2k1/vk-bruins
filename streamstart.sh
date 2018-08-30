#! /bin/bash

cat video | nc.traditional 192.168.1.43 5000 & raspivid -o video -t 0 -w 640 -h 480
