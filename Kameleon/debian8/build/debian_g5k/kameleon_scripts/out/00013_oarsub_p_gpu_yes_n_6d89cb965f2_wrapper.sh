#!/usr/bin/env bash

ROOT_DIRECTORY=$(dirname $(readlink -f ${BASH_SOURCE[0]}))

function post_exec_wrapper {
    echo $? > "$ROOT_DIRECTORY/bash_status"
    # Print end flags
    echo -n __CMD_ERR_13_3377_44940_END__ 1>&2
    echo -n __CMD_OUT_13_3377_44940_END__
}

function pre_exec_wrapper {
    # Print begin flags
    echo -n __CMD_ERR_13_3377_44940_BEGIN__ 1>&2
    echo -n __CMD_OUT_13_3377_44940_BEGIN__
}

trap 'post_exec_wrapper' INT TERM EXIT

## Started
pre_exec_wrapper
bash --rcfile "/home/fpopek/kameleon_workdir/debian_g5k/kameleon_scripts/out/bash_rc" /home/fpopek/kameleon_workdir/debian_g5k/kameleon_scripts/out/00013_oarsub_p_gpu_yes_n_6d89cb965f2.sh

