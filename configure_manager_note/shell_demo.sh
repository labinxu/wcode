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
    for (( i = 1; i <= 3; i++ ))
    do
        for (( j = 1; j <= 3; j++ ))
        do
            tot=`expr $i + $j`
            tmp=`echo $tot % 2 | bc` # `expr $tot % 2`
            if [ $tmp -eq 0 ]; then
                echo -e -n "033[47m "
            else
                echo -e -n "033[40m "
            fi
        done
        echo -e -n "033[40m"
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


function IORedirection()
{
    echo 'Usage:'
    echo "$0 > 5 5"
    echo "$0 1 > &2"

    if [ $# -ne 2 ]; then
        echo "Error: number are not supplied"
        echo "Usage: $0 number1 number2"
        exit 1
    fi
    ans=`expr $1 + $2`
    echo "Sum is $ans"
}
function readfile()
{
    echo "=========================="
    echo "read $0"
    while read line
    do
        result=`echo ${line} |grep "readfile"`
        if [[ ${result} != "" ]]; then
            echo "call the function: ${line}"
        else
            continue
        fi
    done < $0
}

function foreachArray()
{
    echo "=========================="
    echo "foreach the array"
    array="a b c"
    for item in ${array};
    do
        echo ${item}
    done
}

#function handleOption()
#{
    echo "================="
    echo "handle option args"
    while getopts "v:p:hu:" optname
    do
        case "$optname" in
            "v")
                echo "Option $optname have value $OPTARG"
                ;;
            "h")
                echo "Option $optname have value $OPTARG"
                ;;
        esac
        echo "OPTIND is now $OPTIND"
    done
#}

echo "IO redirection demo"
#IORedirection # error print
IORedirection 2 4
readfile
foreachArray
# handleOption
