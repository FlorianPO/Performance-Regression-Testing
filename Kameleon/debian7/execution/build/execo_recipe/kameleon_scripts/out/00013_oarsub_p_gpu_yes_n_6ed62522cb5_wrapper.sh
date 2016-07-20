#!/usr/bin/env bash

ROOT_DIRECTORY=$(dirname $(readlink -f ${BASH_SOURCE[0]}))

function post_exec_wrapper {
    echo $? > "$ROOT_DIRECTORY/bash_status"
    # Print end flags
    echo -n __CMD_ERR_13_7151_333725_END__ 1>&2
    echo -n __CMD_OUT_13_7151_333725_END__
}

function pre_exec_wrapper {
    # Print begin flags
    echo -n __CMD_ERR_13_7151_333725_BEGIN__ 1>&2
    echo -n __CMD_OUT_13_7151_333725_BEGIN__
}

trap 'post_exec_wrapper' INT TERM EXIT

## Started
pre_exec_wrapper
bash --rcfile "/home/fpopek/kameleon_workdir/execo_recipe/kameleon_scripts/out/bash_rc" /home/fpopek/kameleon_workdir/execo_recipe/kameleon_scripts/out/00013_oarsub_p_gpu_yes_n_6ed62522cb5.sh

