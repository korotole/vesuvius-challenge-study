#! /bin/bash

while true; do
    # get only `jpg` files, mind timeout of 15 seconds and continue after it
    wget --recursive --no-parent -T 15 -c https://dl.ash2txt.org/full-scrolls/Scroll1/PHercParis4.volpkg/scroll1_autosegmentation_20241003234631/predictions/ --accept png && break
done
