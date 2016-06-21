#!/usr/bin/env bash

ROOT_DIRECTORY=$(dirname $(readlink -f ${BASH_SOURCE[0]}))

function post_exec_wrapper {
    echo $? > "$ROOT_DIRECTORY/bash_status"
    # Print end flags
    echo -n __CMD_ERR_1_6424_460235_END__ 1>&2
    echo -n __CMD_OUT_1_6424_460235_END__
}

function pre_exec_wrapper {
    # Print begin flags
    echo -n __CMD_ERR_1_6424_460235_BEGIN__ 1>&2
    echo -n __CMD_OUT_1_6424_460235_BEGIN__
}

trap 'post_exec_wrapper' INT TERM EXIT

## Started
pre_exec_wrapper
bash --rcfile "/home/florian/Bureau/Kameleon/build/debian8_g5k/kameleon_scripts/local/bash_rc" /home/florian/Bureau/Kameleon/build/debian8_g5k/kameleon_scripts/local/00001_echo_the_local_context_has_bee.sh

