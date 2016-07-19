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
echo kadeploy3\ -a\ \~/kameleon_workdir/debian_g5k/kameleonImage.env\ -m\ \$machine\ -k >> "${__ROOT_DIRECTORY__}/bash_history"



kadeploy3 -a ~/kameleon_workdir/debian_g5k/kameleonImage.env -m $machine -k

