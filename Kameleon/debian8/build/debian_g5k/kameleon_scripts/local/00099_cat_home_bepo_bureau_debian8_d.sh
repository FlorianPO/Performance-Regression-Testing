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
echo cat\ /home/bepo/Bureau/debian8/default/chroot/steps/data/skel/.vimrc >> "${__ROOT_DIRECTORY__}/bash_history"



cat /home/bepo/Bureau/debian8/default/chroot/steps/data/skel/.vimrc
