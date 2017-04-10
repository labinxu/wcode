#!/bin/bash

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
        "u")
            echo "Option $optname have value $OPTARG"
            exit 0
            ;;
    esac
    echo "OPTIND is now $OPTIND"
done
