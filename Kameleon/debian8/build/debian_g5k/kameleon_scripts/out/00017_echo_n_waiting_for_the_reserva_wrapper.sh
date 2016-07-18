#!/usr/bin/env bash

ROOT_DIRECTORY=$(dirname $(readlink -f ${BASH_SOURCE[0]}))

function post_exec_wrapper {
    echo $? > "$ROOT_DIRECTORY/bash_status"
    # Print end flags
    echo -n __CMD_ERR_17_3377_121801_END__ 1>&2
    echo -n __CMD_OUT_17_3377_121801_END__
}

function pre_exec_wrapper {
    # Print begin flags
    echo -n __CMD_ERR_17_3377_121801_BEGIN__ 1>&2
    echo -n __CMD_OUT_17_3377_121801_BEGIN__
}

trap 'post_exec_wrapper' INT TERM EXIT

## Started
pre_exec_wrapper
bash --rcfile "/home/fpopek/kameleon_workdir/debian_g5k/kameleon_scripts/out/bash_rc" /home/fpopek/kameleon_workdir/debian_g5k/kameleon_scripts/out/00017_echo_n_waiting_for_the_reserva.sh

