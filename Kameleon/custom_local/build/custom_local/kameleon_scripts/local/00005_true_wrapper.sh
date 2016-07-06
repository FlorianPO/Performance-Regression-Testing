#!/usr/bin/env bash

ROOT_DIRECTORY=$(dirname $(readlink -f ${BASH_SOURCE[0]}))

function post_exec_wrapper {
    echo $? > "$ROOT_DIRECTORY/bash_status"
    # Print end flags
    echo -n __CMD_ERR_5_29432_557778_END__ 1>&2
    echo -n __CMD_OUT_5_29432_557778_END__
}

function pre_exec_wrapper {
    # Print begin flags
    echo -n __CMD_ERR_5_29432_557778_BEGIN__ 1>&2
    echo -n __CMD_OUT_5_29432_557778_BEGIN__
}

trap 'post_exec_wrapper' INT TERM EXIT

## Started
pre_exec_wrapper
bash --rcfile "/home/bepo/Bureau/custom_local/build/custom_local/kameleon_scripts/local/bash_rc" /home/bepo/Bureau/custom_local/build/custom_local/kameleon_scripts/local/00005_true.sh

