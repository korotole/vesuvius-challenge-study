#! /bin/bash

while true; do
    wget --recursive --no-parent -T 15 -c https://dl.ash2txt.org/full-scrolls/Scroll5/PHerc172.volpkg/paths/ --accept "jpg" && break
    wget --recursive --no-parent -T 15 -c https://dl.ash2txt.org/full-scrolls/Scroll5/PHerc172.volpkg/paths/ --accept "png" && break
done