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
echo tar\ -cvf\ kameleon_scripts_in.tar\ kameleon_scripts/in/\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \#\ Kameleon\ scripts'
'tar\ -cvf\ starpu_results.tar\ results_\*\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \#\ StarPU\ results >> "${__ROOT_DIRECTORY__}/bash_history"



tar -cvf kameleon_scripts_in.tar kameleon_scripts/in/                   # Kameleon scripts
tar -cvf starpu_results.tar results_*                                   # StarPU results

