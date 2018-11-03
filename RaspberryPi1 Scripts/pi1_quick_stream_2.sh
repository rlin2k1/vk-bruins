#! /bin/bash
: 'pi1_quick_stream_2.sh
Sends Pictures from the Raspberry Pi 1 to the Computer

USAGE: ./pi1_quick_stream_2.sh

Author(s):
    Roy Lin

Date Created:
    October 3rd, 2018
'

cat video | nc.traditional 192.168.0.114 5000 & raspivid -o video -t 0 -w 640 -h 480