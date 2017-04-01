#!/bin/bash

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


# function define
function chessboard ()
{
    for (( i = 1; i <= 9; i++ ))
    do
        for (( j = 1; j <= 9; j++ ))
        do
            tot=`expr $i + $j`
            tmp=`echo $tot % 2 | bc` # `expr $tot % 2`
            if [ $tmp -eq 0 ]; then
                echo -e -n "\033[47m "
            else
                echo -e -n "\033[40m "
            fi
        done
        echo -e -n "\033[40m"
        echo ""
    done
}
echo " Function call   "
chessboard 
#for i < NR #read total lines

echo "awk test.."
awk -F ':' 'BEGIN {count=0;} {name[count] = $1;count++;}; END{for (i = 0; i < 3; i++) print i, name[i]}' /etc/passwd

function casedemo()
{
    rental=$1
    case $rental in
        "car") echo "For $rental Rs.20 per k/m";;
        "van") echo "For $rental Rs.30 per k/m";;
        *) echo "Sorry I can not get a $rental for you";;
    esac
}

echo "for case demo"
casedemo car
