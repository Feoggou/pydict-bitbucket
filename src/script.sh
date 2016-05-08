#!/bin/bash

# dir_path=/home/zenith/Dropbox/Docs/DICTIONARY
dir_path=/home/zenith/dictionary/words

# for x in `ls $dir_path`; do ./py-dict.py $dir_path $x; done
for x in `ls $dir_path`; do
#   if ! [ $(expr match "$x" '.*\(\.json\)') ]; then
    # ./py-dict.py $dir_path $x
    ./main.py $x
    if [[ $? != 0 ]]; then echo "$x" >> fails_new2.txt; fi
#   fi
done


