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
echo echo\ -n\ \"Waiting\ for\ the\ reservation\ to\ be\ ready\"'
'until\ \$\(oarstat\ -fu\ fpopek\ \|\ grep\ -q\ \"state\ \=\ Running\"\)'
'do'
'\ \ echo\ -n\ .'
'\ \ sleep\ 2'
'done'
'sleep\ 1'
'echo\ \"\ \~\>\ OK\" >> "${__ROOT_DIRECTORY__}/bash_history"

set -o xtrace 

echo -n "Waiting for the reservation to be ready"
until $(oarstat -fu fpopek | grep -q "state = Running")
do
  echo -n .
  sleep 2
done
sleep 1
echo " ~> OK"

