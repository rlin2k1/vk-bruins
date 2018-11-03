#! /bin/bash
: 'pi3_quick_stream_2.sh
Sends Pictures from the Raspberry Pi 3 to the Computer

USAGE: ./pi3_quick_stream_2.sh

Author(s):
    Roy Lin

Date Created:
    October 3rd, 2018
'

cat video | nc.traditional 192.168.0.111 5000 & raspivid -o video -t 0 -w 640 -h 480