#!/bin/bash

username=`whoami`
export DISK_DIR=/local/$username/preint
PERL=perl5.87
function module()
{
    echo "[+] inner module $*"
    eval `/p/inway_arch/tools/opensource/Modules/3.2.10-i01/bin/modulecmd bash $*`
}

function printCurrentDir()
{
    currentdir=`pwd`
    echo "Current dir is: ${currentdir}"

}
function initEnv()
{
    if [[ $1 == "" ]];
	then
	echo "[*] Please input correct baseline version..."
	return
    fi
	
    echo "init the opticm environment..."
   
    echo "[+]Enter workspace dir..."
    mkdir -p $DISK_DIR
    cd $DISK_DIR
    echo "[+]create dir : "$1" and enter it.."
    if [ -d $1 ];
    then
        echo "[+] Empty workspace rm -rf ${1}"
        rm -rf $1
    fi
    mkdir $1;cd $1
    export WORKSPACE=`pwd`
    echo "[+] module load artifactory"
    module load artifactory
}

function syncCode()
{
    module load opticm6
    echo "[+] Sync source code ..."
    echo '[+] bee init -p ice7360 -v $1 && bee sync -j16'
    bee init -p ice7360 -v $1 && bee sync -j16
}

function CopyBinFromBender()
{
    if [[ $1 == "" ]];
	then
	echo "[*] Please input bender id..."
	return 1
    fi
    result=`echo $1 | egrep -o "ICE7360_PREINT_BENDER_[0-9]{4}"`
    if [[ $result == "" ]];
	then
	echo "[*] Please input correct bender id.."
	return 1
    fi
    cd ${WORKSPACE}
    printCurrentDir
    module load artifactory
    module unload perl
    module load perl
    perl /home/labinxux/bin/copy_b2e.pl $1 xmm7360
    
}

function RenameTempFolder()
{
    echo "cd ${WORKSPACE}"
    cd ${WORKSPACE}
    printCurrentDir
    # temp_ICE7360_PREINT_BENDER_2333
    OUTPUT="output"
    ICE7360="ICE7360"
    destFolderName=`ls temp_* |head -n 1 | egrep "ICE7360_PREINT_BENDER_[0-9]{4}"`
    echo "Dest folder ${destFolderName}"
    #ICE7360
    echo "[+] Rename folder ..."
    outFolder=`ls | egrep  "temp_" | head -n 1`
    if [ ! -d $outFolder ];
    then
	echo "[*] Error : ${outFolder} not exists"
	exit 1
    fi
    # temp_ICE7360_PREINT_BENDER_2333
    echo "[+] Rename $outfolder to ${OUTPUT}"
    mv $outFolder ${OUTPUT}
    printCurrentDir
    mv "${OUTPUT}/${destFolderName}" "${OUTPUT}/${ICE7360}"
}

function Copy2ShareFolder()
{
    echo "args 1 is preint name eg: ICE7360_05.1718.04_PREINT_WED_03"
    echo "[+] Copy to /nfs/imu/disks/sw_builds/XMM7360/Pre-Int"
    cd `ls -l | egrep -o "temp_ICE7360_PREINT_BENDER_[0-9]{4}"`
    destFolder=`ls -l | egrep -o "ICE7360_PREINT_BENDER_[0-9]{4}"`
    
    if [ ! -d /nfs/imu/disks/sw_builds/XMM7360/Pre-Int/$1 ];
    then
        echo "copy $destFolder to /nfs/imu/disks/sw_builds/XMM7360/Pre-Int/${1}"
        cp -r $destFolder /nfs/imu/disks/sw_builds/XMM7360/Pre-Int/$1
    else
        echo "/nfs/imu/disks/sw_builds/XMM7360/Pre-Int/${1} already exist"
    fi
    echo "[+] Change to ${WORKSPACE}"
    cd ${WORKSPACE}
}
function getCherryPicks()
{
    details=`curl https://oc6web.intel.com/bender/search/$1`
    url=`echo $details | egrep $1 | egrep -o /bender/details/[0-9]{5}`
    echo "curl https://oc6web.intel.com/bender/search/"$1" | egrep "$1" | egrep -o /bender/details/[0-9]{5}"
    detailurl=https://oc6web.intel.com$url
    echo "[+] DETAILS URL IS: "detailurl
    details=`curl $detailurl`
    patchs=`echo $details | egrep CHANGES | egrep -o [0-9]{6}/[0-9]{1} | sort |  uniq`
    echo $patchs
    export PATCHS=$patchs

}
function CherryPick()
{
    echo "[+] CherryPick: "$1
    getCherryPicks $1
    echo "[+] PATCHS : "$PATCHS
    bee download -c $PATCHS
}

function TriggerHarts()
{
    echo "[+] Trigger Harts beging.."
    cd ${WORKSPACE}
    printCurrentDir
    echo "param is PREINT ID ..."
    cd  modem/system-build/product
    if [ -f "submit_harts_jobs.sh" ];
    then
	echo "Trigger file is ok"
    fi
    module unload python
    module load python
    ./submit_harts_jobs.sh $1 PREINT_ICE7360
    printCurrentDir
    echo "[+] Trigger Harts end.."
}
function Trigger3GW()
{
    cd ${WORKSPACE}
    # param 1: preintId
    version=`echo $1 | awk -F_ '{print $2}'`
    #05.1717.05
    RBN=${version:4:3}
    UBN=${version:9:1}
    echo "Trigger 3GW --RBN ${RBN} --UBN ${UBN} --FILENAME ${1}"
    cd fw_3g/xmm7360/umts_fw_dev/tools/integration_mgt/common/scripts/oc6
    printCurrentDir
    echo "[+] Init oc6env "
    oc6env
   # 1 preint id
    ./FW3G_GC_SUBMITTER_UBS.sh --PROJECT XMM7360 --SYSTARGET XMM7360_REV_2.1_NAND --EB no --RELEASE yes --FORCEREBUILD yes --TESTSUITE full --REGRESSION gc --RBN $RBN --UBN $UBN --FILENAME $1
}
function start()
{
    # ver=`echo "ICE7360_05.1718.04_PREINT_WED_02" | awk -F . '{print $2}'`
    # 1 Preint Id ICE7360_05.1718.04_PREINT_WED_03
    preintId=`echo $1 | egrep -o "ICE7360_05\.[0-9]{4}\.[0-9]{2}_PREINT_[A-Z]{3}_[0-9]{2}"`
    if [[ $preintId == "" ]];
	then
	echo "[*] Please input correct preint id.."
	return
    fi
    echo "PREINT ID IS: "$preintId
    # 1 baseline
    baseline=`echo $preintId | egrep -o "ICE7360_05\.[0-9]{4}\.[0-9]{2}"`
    if [[ $baseline == "" ]];
    then
	echo "[*]Please input correct preint id..." $1
	return
    fi
    echo "BASELINE IS: "$baseline
    # 2 bender id
    benderId=`echo $2 | egrep -o "ICE7360_PREINT_BENDER_[0-9]{4}"`
    if [[ $benderId == "" ]];
	then
	echo "[*] Please input correct bender id.."
	return
    fi
    echo "BENDER ID IS: "$benderId

    initEnv $baseline
    syncCode $baseline
    CherryPick $preintId
    
    CopyBinFromBender $benderId
    Copy2ShareFolder $preintId
    RenameTempFolder
    TriggerHarts $preintId
    
}

function testpreint()
{
#    export WORKSPACE=`pwd`
 #   cd bin
  #  echo `pwd`
   # echo "Current dir is : `pwd`"
    #cd ${WORKSPCE}
    #echo "Current dir is : ${WORKSPACE}"
    module load opticm6
    source oc6env
    echo "last return" $?
}

set -v
start $1 $2
