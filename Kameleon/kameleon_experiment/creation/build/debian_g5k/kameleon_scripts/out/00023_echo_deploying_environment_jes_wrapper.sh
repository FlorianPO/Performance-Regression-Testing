#!/usr/bin/env bash

ROOT_DIRECTORY=$(dirname $(readlink -f ${BASH_SOURCE[0]}))

function post_exec_wrapper {
    echo $? > "$ROOT_DIRECTORY/bash_status"
    # Print end flags
    echo -n __CMD_ERR_23_6059_227624_END__ 1>&2
    echo -n __CMD_OUT_23_6059_227624_END__
}

function pre_exec_wrapper {
    # Print begin flags
    echo -n __CMD_ERR_23_6059_227624_BEGIN__ 1>&2
    echo -n __CMD_OUT_23_6059_227624_BEGIN__
}

trap 'post_exec_wrapper' INT TERM EXIT

## Started
pre_exec_wrapper
bash --rcfile "/home/fpopek/kameleon_workdir/debian_g5k/kameleon_scripts/out/bash_rc" /home/fpopek/kameleon_workdir/debian_g5k/kameleon_scripts/out/00023_echo_deploying_environment_jes.sh

