#/usr/bin/bash
if [ -d bugtracker ]; then
    echo "bugtracker exist"
    rsync -a --progress harman_aosp@10.239.93.58:/home/harman_aosp/BugTrackingTable.xlsx ./bugtracker/
else
    mkdir bugtracker
fi
