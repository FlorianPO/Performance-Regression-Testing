#!/usr/bin/env bash

ROOT_DIRECTORY=$(dirname $(readlink -f ${BASH_SOURCE[0]}))

function post_exec_wrapper {
    echo $? > "$ROOT_DIRECTORY/bash_status"
    # Print end flags
    echo -n __CMD_ERR_11_6059_208060_END__ 1>&2
    echo -n __CMD_OUT_11_6059_208060_END__
}

function pre_exec_wrapper {
    # Print begin flags
    echo -n __CMD_ERR_11_6059_208060_BEGIN__ 1>&2
    echo -n __CMD_OUT_11_6059_208060_BEGIN__
}

trap 'post_exec_wrapper' INT TERM EXIT

## Started
pre_exec_wrapper
bash --rcfile "/home/fpopek/kameleon_workdir/debian_g5k/kameleon_scripts/out/bash_rc" /home/fpopek/kameleon_workdir/debian_g5k/kameleon_scripts/out/00011_echo_submitting_a_job_for_depl.sh

