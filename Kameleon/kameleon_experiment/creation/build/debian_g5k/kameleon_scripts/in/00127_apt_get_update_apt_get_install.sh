#!/usr/bin/env bash

set -o pipefail
set -o allexport

__ROOT_DIRECTORY__=$(dirname $(readlink -f ${BASH_SOURCE[0]}))

function save_env {
    # Save environment
    set +x
    (comm -3 <(declare | sort) <(declare -f | sort)) > "${__ROOT_DIRECTORY__}/bash_env"
}

trap 'save_env' INT TERM EXIT

# Load environment
source "${__ROOT_DIRECTORY__}/bash_env" 2> /dev/null || true

# Log cmd
echo apt-get\ update'
'apt-get\ install\ -y\ python2.7-dev\ python-httplib2\ python-pip'
'apt-get\ install\ -y\ vim\ emacs'
'apt-get\ install\ -y\ curl\ patch'
'apt-get\ install\ -y\ git\ subversion\ mercurial'
'apt-get\ install\ -y\ build-essential\ gfortran'
'apt-get\ install\ -y\ autoconf\ automake\ cmake\ cmake-data\ doxygen\ texinfo'
'apt-get\ install\ -y\ libtool'
'apt-get\ install\ -y\ libboost-dev'
'apt-get\ install\ -y\ gawk'
'apt-get\ install\ -y\ bison\ flex'
'apt-get\ install\ -y\ binutils-dev\ libelf-dev\ libiberty-dev'
'apt-get\ install\ -y\ libz-dev'
'apt-get\ install\ -y\ libqt4-dev\ freeglut3-dev'
'apt-get\ install\ -y\ environment-modules'
'apt-get\ install\ -y\ hwloc\ libhwloc-dev >> "${__ROOT_DIRECTORY__}/bash_history"

set -o xtrace 

apt-get update
apt-get install -y python2.7-dev python-httplib2 python-pip
apt-get install -y vim emacs
apt-get install -y curl patch
apt-get install -y git subversion mercurial
apt-get install -y build-essential gfortran
apt-get install -y autoconf automake cmake cmake-data doxygen texinfo
apt-get install -y libtool
apt-get install -y libboost-dev
apt-get install -y gawk
apt-get install -y bison flex
apt-get install -y binutils-dev libelf-dev libiberty-dev
apt-get install -y libz-dev
apt-get install -y libqt4-dev freeglut3-dev
apt-get install -y environment-modules
apt-get install -y hwloc libhwloc-dev

