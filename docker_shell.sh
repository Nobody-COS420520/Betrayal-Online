#!/bin/sh
CMD="$1"


echo '\n*******************************************************\n'
echo 'Deleting old a.py'
rm -f a.py
echo 'Concatenating /src/*.py into a.py'
cat ./src/*.py >> a.py
echo "Concatenating ${CMD} into a.py"
cat $CMD >> a.py
echo 'Concatenation Complete'
#cat a.py
#ls
echo '\n*******************************************************\n'
pylint a.py
echo '\n*******************************************************\n'
echo 'pytest output would usually take this space'
#pytest ./tests/tests.py
echo '\n*******************************************************\n'


pgzrun a.py