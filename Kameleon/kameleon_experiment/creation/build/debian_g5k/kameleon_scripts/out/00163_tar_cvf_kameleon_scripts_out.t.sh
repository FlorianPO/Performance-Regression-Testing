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
echo tar\ -cvf\ kameleon_scripts_out.tar\ kameleon_scripts/out/\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \#\ Kameleon\ scripts'
'tar\ -cvf\ OAR_logs.tar\ \$\(find\ .\ -name\ \"OAR.\*.\$\(cat\ job_id\).\*\"\)\ \ \ \ \ \ \ \ \ \ \ \#\ OAR\ logs >> "${__ROOT_DIRECTORY__}/bash_history"

set -o xtrace 

tar -cvf kameleon_scripts_out.tar kameleon_scripts/out/                 # Kameleon scripts
tar -cvf OAR_logs.tar $(find . -name "OAR.*.$(cat job_id).*")           # OAR logs

