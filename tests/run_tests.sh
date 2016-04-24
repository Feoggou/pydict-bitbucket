nosetests3

for x in `ls`; do if [ -d $x ]; then nosetests3 -w $x; fi; done
