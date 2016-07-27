#!/usr/bin/env bash

ROOT_DIRECTORY=$(dirname $(readlink -f ${BASH_SOURCE[0]}))

function post_exec_wrapper {
    echo $? > "$ROOT_DIRECTORY/bash_status"
    # Print end flags
    echo -n __CMD_ERR_45_7127_262820_END__ 1>&2
    echo -n __CMD_OUT_45_7127_262820_END__
}

function pre_exec_wrapper {
    # Print begin flags
    echo -n __CMD_ERR_45_7127_262820_BEGIN__ 1>&2
    echo -n __CMD_OUT_45_7127_262820_BEGIN__
}

trap 'post_exec_wrapper' INT TERM EXIT

## Started
pre_exec_wrapper
bash --rcfile "/root/kameleon_workdir/execo_recipe/kameleon_scripts/in/bash_rc" /root/kameleon_workdir/execo_recipe/kameleon_scripts/in/00045_cat_kameleon_workdir_pipe_cat_.sh
