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
echo echo\ \"Deploying\ image\ \~/kameleon_workdir/debian_g5k/kameleonImage.env\ with\ kadeploy\" >> "${__ROOT_DIRECTORY__}/bash_history"



echo "Deploying image ~/kameleon_workdir/debian_g5k/kameleonImage.env with kadeploy"

