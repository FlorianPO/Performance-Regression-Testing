#!/usr/bin/env bash

ROOT_DIRECTORY=$(dirname $(readlink -f ${BASH_SOURCE[0]}))

function post_exec_wrapper {
    echo $? > "$ROOT_DIRECTORY/bash_status"
    # Print end flags
    echo -n __CMD_ERR_121_6059_412362_END__ 1>&2
    echo -n __CMD_OUT_121_6059_412362_END__
}

function pre_exec_wrapper {
    # Print begin flags
    echo -n __CMD_ERR_121_6059_412362_BEGIN__ 1>&2
    echo -n __CMD_OUT_121_6059_412362_BEGIN__
}

trap 'post_exec_wrapper' INT TERM EXIT

## Started
pre_exec_wrapper
bash --rcfile "/root/kameleon_workdir/debian_g5k/kameleon_scripts/in/bash_rc" /root/kameleon_workdir/debian_g5k/kameleon_scripts/in/00121_useradd_m_kameleon_s_bin_bash.sh

