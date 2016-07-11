#!/usr/bin/env bash

ROOT_DIRECTORY=$(dirname $(readlink -f ${BASH_SOURCE[0]}))

function post_exec_wrapper {
    echo $? > "$ROOT_DIRECTORY/bash_status"
    # Print end flags
    echo -n __CMD_ERR_29_9792_39699_END__ 1>&2
    echo -n __CMD_OUT_29_9792_39699_END__
}

function pre_exec_wrapper {
    # Print begin flags
    echo -n __CMD_ERR_29_9792_39699_BEGIN__ 1>&2
    echo -n __CMD_OUT_29_9792_39699_BEGIN__
}

trap 'post_exec_wrapper' INT TERM EXIT

## Started
pre_exec_wrapper
bash --rcfile "/home/bepo/Bureau/custom/build/custom_debian_g5k/kameleon_scripts/local/bash_rc" /home/bepo/Bureau/custom/build/custom_debian_g5k/kameleon_scripts/local/00029_cat_kameleon_workdir_pipe_cat_.sh

