#!/usr/bin/env bash

set -o pipefail
set -o allexport

__ROOT_DIRECTORY__=$(dirname $(readlink -f ${BASH_SOURCE[0]}))

function save_env {
    # Save environment
    
    (comm -3 <(declare | sort) <(declare -f | sort)) > "${__ROOT_DIRECTORY__}/bash_env"
}

trap 'save_env' INT TERM EXIT

# Load environment
source "${__ROOT_DIRECTORY__}/bash_env" 2> /dev/null || true

# Log cmd
echo tar\ -xvf\ kameleon_scripts_out.tar'
'rm\ kameleon_scripts_out.tar'
'tar\ -xvf\ OAR_logs.tar'
'rm\ OAR_logs.tar >> "${__ROOT_DIRECTORY__}/bash_history"



tar -xvf kameleon_scripts_out.tar
rm kameleon_scripts_out.tar
tar -xvf OAR_logs.tar
rm OAR_logs.tar

