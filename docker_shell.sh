#!/bin/sh
CMD="$1"
flag=0

echo '\n*******************************************************\n'
pylint ./src/
echo '\n*******************************************************\n'
#pytest ./tests/tests.py
echo '\n*******************************************************\n'
if [ "$flag" -eq 0 ]
then
	cat ./src/*.py >> a.py
	cat $CMD >> a.py
	flag=1
fi
cat a.py
pgzrun a.py