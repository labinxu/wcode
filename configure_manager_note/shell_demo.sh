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

function handleOption()
{
    echo "================="
    echo "handle option args"
    while getopts "v:p:h:u:" optname
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
}
function seddemo()
{
    echo '========================================='
    echo 'sed command demo'
    cat $0 -n | sed -n '1,3p' #print line1-line3
    cat $0 -n | sed -n '1~2p' #print line (1,3,5,...)
    cat $0 -n | sed -n '1!d'
    # s search and replace
    # '[address]s/pattern/replacement/flags'
    # flags : g full repace, p print ,w saveas
    # cat gbkdemo.txt -n | sed -n '5s/line/nine/p'
    cat $0 -n | sed -n '1!d'
    # save as to saveas
    cat gbkdemo.txt -n | sed -n 's/line/nine/gw ./saveas'
    sed 's/^.//1' gbkdemo.txt # remove first char from lines
    sed '1i hello' gbkdemo.txt # insert hello front the line 1
    sed '1a hello' gbkdemo.txt # insert hello back the line 1
    echo "loveablelove" | sed 's/\(love\)able/\1=' #
    echo "10100010" | sed 's#10#100#g' # replace 10 to 100
}

echo "IO redirection demo"
#IORedirection # error print
IORedirection 2 4
readfile
foreachArray
handleOption
seddemo
