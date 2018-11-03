#! /bin/bash
: 'pi1_quick_stream_1.sh
Receives Pictures from the Raspberry Pi 1 and Outputs them into a Video Frame

USAGE: ./pi1_quick_stream_1.sh

Author(s):
    Roy Lin

Date Created:
    October 3rd, 2018
'

netcat -l -p 5000 | mplayer -fps 60 -cache 1024 -