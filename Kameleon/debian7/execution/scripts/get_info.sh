#!/bin/bash
# Script for to get machine information before doing the experiment

set +e # Don't fail fast since some information is maybe not available

title="Experiment results"
starpu_build=""
inputfile=""
host="$(hostname | sed 's/[0-9]*//g' | cut -d'.' -f1)"
help_script()
{
    cat << EOF
Usage: $0 [options] outputfile.org

Script for to get machine information before doing the experiment

OPTIONS:
   -h      Show this message
   -t      Title of the output file
   -s      Path to the StarPU installation
   -i      Input file name if doing SimGrid simulation based on input
EOF
}
# Parsing options
while getopts "t:s:i:h" opt; do
    case $opt in
	t)
	    title="$OPTARG"
	    ;;
	s)
	    starpu_build="$OPTARG"
	    ;;
	i)
	    inputfile="$OPTARG"
	    ;;
	h)
	    help_script
	    exit 4
	    ;;
	\?)
	    echo "Invalid option: -$OPTARG"
	    help_script
	    exit 3
	    ;;
    esac
done

shift $((OPTIND - 1))
filedat=$1
if [[ $# != 1 ]]; then
    echo 'ERROR!'
    help_script
    exit 2
fi

##################################################
# Preambule of the output file
echo "#+TITLE: $title" >> $filedat
echo "#+DATE: $(eval date)" >> $filedat
echo "#+AUTHOR: $(eval whoami)" >> $filedat
echo "#+MACHINE: $(eval hostname)" >> $filedat
echo "#+FILE: $(eval basename $filedat)" >> $filedat
if [[ -n "$inputfile" ]]; 
then
    echo "#+INPUTFILE: $inputfile" >> $filedat
fi
echo " " >> $filedat 

##################################################
# Collecting metadata
echo "* MACHINE INFO:" >> $filedat

echo "** PEOPLE LOGGED WHEN EXPERIMENT STARTED:" >> $filedat
who >> $filedat
echo "############################################" >> $filedat

echo "** ENVIRONMENT VARIABLES:" >> $filedat
env >> $filedat
echo "############################################" >> $filedat

echo "** HOSTNAME:" >> $filedat
hostname >> $filedat
echo "############################################" >> $filedat

if [[ -n $(command -v lstopo) ]];
then
    echo "** MEMORY HIERARCHY:" >> $filedat
    lstopo --of console >> $filedat
    echo "############################################" >> $filedat
fi

if [[ -n "$starpu_build" ]]; 
then
    echo "** STARPU MACHINE DISPLAY:" >> $filedat
    $starpu_build/tools/starpu_machine_display 1> tmp 2> /dev/null
    cat tmp >> $filedat
    rm -f tmp
    echo "############################################" >> $filedat
fi

if [ -f /proc/cpuinfo ];
then
    echo "** CPU INFO:" >> $filedat
    cat /proc/cpuinfo >> $filedat
    echo "############################################" >> $filedat
fi

if [ -f /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor ];
then
    echo "** CPU GOVERNOR:" >> $filedat
    cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor >> $filedat
    echo "############################################" >> $filedat
fi

if [ -f /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq ];
then
    echo "** CPU FREQUENCY:" >> $filedat
    cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq >> $filedat
    echo "############################################" >> $filedat
fi


if [[ -n $(command -v nvidia-smi) ]];
then
    echo "** GPU INFO FROM NVIDIA-SMI:" >> $filedat
    nvidia-smi -q >> $filedat
    echo "############################################" >> $filedat
fi 

if [ -f /proc/version ];
then
    echo "** LINUX AND GCC VERSIONS:" >> $filedat
    cat /proc/version >> $filedat
    echo "############################################" >> $filedat
fi

if [[ -n $(command -v module) ]];
then
    echo "** MODULES:" >> $filedat
    module list 2>> $filedat
    echo "############################################" >> $filedat
fi

##################################################
# Collecting revisions info 
echo "* CODE REVISIONS:" >> $filedat

git_exists=`git rev-parse --is-inside-work-tree`
if [ "${git_exists}" ]
then
    echo "** GIT REVISION OF REPOSITORY:" >> $filedat
    git log -1 >> $filedat
    echo "############################################" >> $filedat
fi

svn_exists=`svn info . 2> /dev/null`
if [ -n "${svn_exists}" ]
then
   echo "** SVN REVISION OF REPOSITORY:" >> $filedat
   svn info >> $filedat
   echo "############################################" >> $filedat
fi

##################################################
# Part specific to the StarPU+SimGrid use case
if [[ -n "$starpu_build" ]]; 
then
    echo "** SIMGRID VERSION:" >> $filedat
    grep "SIMGRID_VERSION_STRING" src/simgrid/SIMGRID/include/simgrid_config.h | sed 's/.*"\(.*\)"[^"]*$/\1/' >> $filedat
    if [[ "$host" == winnetou ]]; then
	git-subrepo status >> $filedat
    fi
    echo "############################################" >> $filedat
    echo "** SVN REVISION OF ORIGINAL STARPU CODE:" >> $filedat
    svn info $starpu_build/.. >> $filedat    
    echo "############################################" >> $filedat    
fi
