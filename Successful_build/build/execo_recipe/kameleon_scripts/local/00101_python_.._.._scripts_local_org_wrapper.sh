#!/usr/bin/env bash

ROOT_DIRECTORY=$(dirname $(readlink -f ${BASH_SOURCE[0]}))

function post_exec_wrapper {
    echo $? > "$ROOT_DIRECTORY/bash_status"
    # Print end flags
    echo -n __CMD_ERR_101_4215_285954_END__ 1>&2
    echo -n __CMD_OUT_101_4215_285954_END__
}

function pre_exec_wrapper {
    # Print begin flags
    echo -n __CMD_ERR_101_4215_285954_BEGIN__ 1>&2
    echo -n __CMD_OUT_101_4215_285954_BEGIN__
}

trap 'post_exec_wrapper' INT TERM EXIT

## Started
pre_exec_wrapper
bash --rcfile "/home/bepo/Bureau/debian7/execution/build/execo_recipe/kameleon_scripts/local/bash_rc" /home/bepo/Bureau/debian7/execution/build/execo_recipe/kameleon_scripts/local/00101_python_.._.._scripts_local_org.sh

