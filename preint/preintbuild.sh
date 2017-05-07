#!/bin/bash
username=`whoami`
export DISK_DIR=/local/$username/preint

function module()
{
    echo "[+] inner module $*"
    eval `/p/inway_arch/tools/opensource/Modules/3.2.10-i01/bin/modulecmd bash $*`
}

function initEnv()
{
    if [[ $1 == "" ]];
	then
	echo "[*] Please input correct baseline version..."
	return
    fi
	
    echo "init the opticm environment..."
    module load opticm6
    echo "[+]Enter workspace dir..."
    mkdir -p $DISK_DIR
    cd $DISK_DIR
    echo "[+]create dir : "$1" and enter it.."
    mkdir $1;cd $1
    export WORKSPACE=`pwd`
    echo "[+] Sync source code ..."
    echo '[+] bee init -p ice7360 -v $1 && bee sync -j16'
    bee init -p ice7360 -v $1 && bee sync -j16
    echo "[+] module load artifactory"
    module load artifactory
    echo "[+] module unload perl;module load perl"
    module unload perl;module load perl

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


    perl /home/labinxux/bin/copy_b2e.pl $1 xmm7360
}

function RenameTempFolder()
{
    destFolderName=`ls temp_* |head -n 1 | egrep "ICE7360_PREINT_BENDER_[0-9]{4}"`
    echo "[+] Rename folder"
    outFolder=`ls  | egrep  "temp_" | head -n 1`
    echo "[+] Rename $outfolder to output"
    mv $outFolder output
}

function Copy2ShareFolder()
{
    echo "args 1 is preint name eg: ICE7360_05.1718.04_PREINT_WED_03"
    echo "[+] Copy to /nfs/imu/disks/sw_builds/XMM7360/Pre-Int"
    cd `ls -l | egrep -o "temp_ICE7360_PREINT_BENDER_[0-9]{4}"`
    destFolder=`ls -l | egrep -o "ICE7360_PREINT_BENDER_[0-9]{4}"`
    echo "copy $destFolder to /nfs/imu/disks/sw_builds/XMM7360/Pre-Int/$1"
    cp -r $destFolder /nfs/imu/disks/sw_builds/XMM7360/Pre-Int/$1
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
    echo "param is PREINT ID ..."
    cd  modem/system-build/product
 # PREINT ID ICE7360_05.1716.05_PREINT_THU_05
    ./submit_harts_jobs.sh $1 PREINT_ICE7360
    echo "[+] Change directory to ${WORKSPACE}"
    cd ${WORKSPACE}
    echo "[+] Trigger Harts end.."
}
function Trigger3GW()
{
   # 1 preint id
    rbn=
    ./FW3G_GC_SUBMITTER_UBS.sh --PROJECT XMM7360 --SYSTARGET XMM7360_REV_2.1_NAND --EB no --RELEASE yes --FORCEREBUILD yes --TESTSUITE full --REGRESSION gc --RBN $2 --UBN $3 --FILENAME $1
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
    
    CherryPick $preintId
    
    CopyBinFromBender $benderId
    Copy2ShareFolder $preintId

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
