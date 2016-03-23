#!/bin/bash

dir_path=/home/zenith/Dropbox/Docs/DICTIONARY
# for x in `ls $dir_path`; do ./py-dict.py $dir_path $x; done
for x in `ls $dir_path`; do
  if ! [ $(expr match "$x" '.*\(\.json\)') ]; then
    ./py-dict.py $dir_path $x
    if [[ $? != 0 ]]; then echo "$x" >> fails.txt; fi
  fi
done


