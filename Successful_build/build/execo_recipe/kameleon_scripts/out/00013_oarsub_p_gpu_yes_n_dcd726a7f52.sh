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
echo oarsub\ -p\ \"gpu\=\'YES\'\"\ -n\ \"dcd726a7f522\"\ -l\ nodes\=1,walltime\=2:00:00\ -t\ deploy\ \"sleep\ 1000000\" >> "${__ROOT_DIRECTORY__}/bash_history"



oarsub -p "gpu='YES'" -n "dcd726a7f522" -l nodes=1,walltime=2:00:00 -t deploy "sleep 1000000"

