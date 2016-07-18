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
echo export\ machine\=\`oarstat\ -fu\ fpopek\ \|\ grep\ assigned_hostnames\ \|\ tail\ -n\ 1\ \|\ cut\ -d\ \'\ \'\ -f\ 7\` >> "${__ROOT_DIRECTORY__}/bash_history"

set -o xtrace 

export machine=`oarstat -fu fpopek | grep assigned_hostnames | tail -n 1 | cut -d ' ' -f 7`

