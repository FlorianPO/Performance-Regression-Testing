#!/usr/bin/env bash

ROOT_DIRECTORY=$(dirname $(readlink -f ${BASH_SOURCE[0]}))

function post_exec_wrapper {
    echo $? > "$ROOT_DIRECTORY/bash_status"
    # Print end flags
    echo -n __CMD_ERR_147_6059_289732_END__ 1>&2
    echo -n __CMD_OUT_147_6059_289732_END__
}

function pre_exec_wrapper {
    # Print begin flags
    echo -n __CMD_ERR_147_6059_289732_BEGIN__ 1>&2
    echo -n __CMD_OUT_147_6059_289732_BEGIN__
}

trap 'post_exec_wrapper' INT TERM EXIT

## Started
pre_exec_wrapper
bash --rcfile "/root/kameleon_workdir/debian_g5k/kameleon_scripts/in/bash_rc" /root/kameleon_workdir/debian_g5k/kameleon_scripts/in/00147_rm_rf_var_lib_apt_lists.sh

