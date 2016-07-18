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
echo cat\ \$\{KAMELEON_WORKDIR\}/pipe-cat_ssh_config_out\ \|\ cat\ \>\ ssh_config_out\ \&\&\ rm\ \$\{KAMELEON_WORKDIR\}/pipe-cat_ssh_config_out >> "${__ROOT_DIRECTORY__}/bash_history"

set -o xtrace 

cat ${KAMELEON_WORKDIR}/pipe-cat_ssh_config_out | cat > ssh_config_out && rm ${KAMELEON_WORKDIR}/pipe-cat_ssh_config_out

