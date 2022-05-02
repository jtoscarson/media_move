#!/bin/sh
cd "$(dirname "$0")";
CWD="$(pwd)"
echo $CWD
/usr/bin/python3 /home/jtoscarson/scripts/media_mover/init.py
