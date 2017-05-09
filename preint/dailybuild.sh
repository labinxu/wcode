#!/bin/bash

username=`whoami`
export DISK_DIR=/local/$username/dailybuild
SHARE_FOLDER_ROOT=/nfs/imu/disks/sw_builds/XMM7360/Release/MODEM
PERL=perl5.87
#_05.1720/MAIN/
function module()
{
    echo "[+] inner module $*"
    eval `/p/inway_arch/tools/opensource/Modules/3.2.10-i01/bin/modulecmd bash $*`
}

function init()
{
    echo "[+]===========INIT WORKSPACE======="
    echo "perl is ${PERL}"
    #source enter_oc6
    mkdir -p $DISK_DIR
    cd $DISK_DIR
    echo "[+]create dir : "$1" and enter it.."
    if [ ! -d ${buildname} ];
       then
	   mkdir ${buildname}
    fi
    cd ${buildname}
    export WORKSPACE=`pwd`
    
    getShareFolderModemDir $1
}
function getShareFolderModemDir()
{
    echo "[+] ==========modem verion name======"
    ver=`echo $1 | egrep -o "_[0-9]{2}\.[0-9]{4}"`
    if [[ $ver == "" ]];
    then
	echo "[*] Please input correct buildname ${1}"
	exit 1
    fi
    export SHARE_FOLDER_ROOT="${SHARE_FOLDER_ROOT}${ver}/MAIN"
    echo "Share folder is: ${SHARE_FOLDER_ROOT}"
}
function CopyBinToShareFolder()
{
    if [[ $1 == "" ]];
	then
	echo "[*] Please input buildname ..."
	return 1
    fi
    echo "[+] ========== Copy ${1} to share folder.."
    #already copied to \\musdsara001.imu.intel.com\sw_builds\XMM7360\Release\MODEM_05.1720\MAIN
    echo "[+] module load artifactory"
    module load artifactory

    echo "[+] run : perl /nfs/imu/disks/sw_builds/XMM7360/Docs/Tools/copy_a2s.pl ${1}"
    perl /nfs/imu/disks/sw_builds/XMM7360/Docs/Tools/copy_a2s.pl $1
}
function RenamePREPFolder()
{
    echo "[+] =========RENAME PREP============"
    cd ${SHARE_FOLDER_ROOT}
    printCurrentDir
    if [ -d ${1}_IN_PREP ];
    then
	echo "[+] Rename ${1}_IN_PREP to ${1}"
	mv ${1}_IN_PREP ${1}
	chmod -R 777 ${1}
    else
	echo "Error: Folder not exists ${SHARE_FOLDER_ROOT}/${1}_IN_PREP"
	exit 1
    fi
}

function printCurrentDir()
{
    currentdir=`pwd`
    echo "Current dir is: ${currentdir}"

}

function genDiffFileAndCopy2ShareFolder()
{
    printCurrentDir
    # echo "[+] module load artifactory"
    # module load artifactory
    # echo "[+] module unload perl;module load perl"
    # module unload perl;module load perl

    echo "[+] mkdir releasecontent"

    if [ ! -d "releasecontent" ];
    then
	mkdir releasecontent
    fi

    cd releasecontent
    printCurrentDir
    ${PERL} -I/nfs/imu/disks/sw_builds/XMM7360/Docs/Tools/perllib/ /nfs/imu/disks/sw_builds/XMM7360/Docs/Tools/relnotes.pl -proj=XMM7360 -release=${1} -utpfile=../../ishare.txt -xmlfile=../../ReleaseContent_XMM7360.xml
    printCurrentDir 
    echo "Copy ${1}.xls to ${SHARE_FOLDER_ROOT}/${1}/${1}.xls"
    if [ ! -f ${1} ];
    then
	sleep 3
    fi
    cp ${1}.xls "${SHARE_FOLDER_ROOT}/${1}/${1}.xls"
    chmod 777 "${SHARE_FOLDER_ROOT}/${1}/${1}.xls"

}
function syncCode()
{
    echo "[+] ==== SYNC CODE======="
    echo "init the opticm environment..."
    cd ${WORKSPACE}
    printCurrentDir
    echo "[+] module load opticm6"
    module load opticm6
    echo "[+]Enter workspace dir..."
    echo "[+] Sync source code ..."
    echo '[+] bee init -p ice7360 -v ${1} && bee sync -j16'
    bee init -p ice7360 -v $1 && bee sync -j16

}
function start()
{
    if [[ $2 == "debug" ]];
    then
	echo $1
	exit 1
    fi

    printCurrentDir
    # verify the buildname
    buildname=`echo ${1} | egrep -o "ICE7360_[0-9]{2}\.[0-9]{4}\.[0-9]{2}"`
    if [[ ${buildname} == "" ]];
	then
	    echo "[*] Please input correct buildname ..."
	    exit 1
    fi

    init ${buildname}
    CopyBinToShareFolder ${buildname}
    RenamePREPFolder ${buildname}
    syncCode ${buildname}
    genDiffFileAndCopy2ShareFolder ${buildname}
}

function testgendiff()
{
    init $1
    genDiffFileAndCopy2ShareFolder $1
}

#start $1

function testdailybuild()
{
    echo $1
}
set -v
start $1 $2
