#!/bin/sh


#read name
#echo "hello $name"
echo "first argument $0"
echo 1+2 | bc
if [ $1 -gt 0 ]; then
    echo "argument larger than zero"
fi
while [ $1 -gt 0 ];do
    echo "do while"
    break
done
